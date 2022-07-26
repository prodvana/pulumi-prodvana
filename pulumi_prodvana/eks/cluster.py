from typing import List, Optional, Sequence

import pulumi_aws as aws
import pulumi_eks as eks

import pulumi_kubernetes as k8s
from pulumi import ComponentResource, Input, Resource, ResourceOptions

from pulumi_prodvana.service_accounts import ProdvanaServiceAccounts
from pulumi_prodvana.services import CertManager, Flagger, Istio

SUBNET_CIDRS = [
    "172.30.0.0/20",
    "172.30.16.0/20",
    "172.30.32.0/20",
    "172.30.48.0/20",
    "172.30.64.0/20",
    "172.30.80.0/20",
    "172.30.96.0/20",
    "172.30.112.0/20",
    "172.30.128.0/20",
    "172.30.144.0/20",
    "172.30.160.0/20",
    "172.30.176.0/20",
    "172.30.192.0/20",
    "172.30.208.0/20",
    "172.30.224.0/20",
]


class EKSCluster(ComponentResource):
    def __init__(
        self,
        name: str,
        region: Input[str],
        nodepool_zones: Input[Sequence[str]],
        node_count_per_zone: Input[int],
        instance_type: Input[str],
        account_id: Optional[Input[str]] = None,
        assume_role_arn: Optional[Input[str]] = None,
        access_key: Optional[Input[str]] = None,
        secret_key: Optional[Input[str]] = None,
        prodvana_managed: bool = True,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__("pvn-cluster:index:Cluster", name, None, opts)

        self.region = region
        aws_provider = aws.Provider(
            "aws",
            region=region,
            allowed_account_ids=[account_id] if account_id else None,
            assume_role=aws.ProviderAssumeRoleArgs(
                role_arn=assume_role_arn,
            )
            if assume_role_arn
            else None,
            access_key=access_key,
            secret_key=secret_key,
        )

        cluster_name = f"pvn-k8s-{name}"
        if len(cluster_name) > 38:
            # {cluster_name}-instanceRole-role-XXXXXXX should be at most 64 chars long
            cluster_name = cluster_name[:38]

        vpc = aws.ec2.Vpc(
            f"pvn-k8s-vpc-{name}",
            cidr_block="172.30.0.0/16",
            enable_dns_hostnames=True,
            opts=ResourceOptions(
                parent=self,
                providers=[aws_provider],
            ),
        )

        igw = aws.ec2.InternetGateway(
            f"pvn-igw-{name}",
            vpc_id=vpc.id,
            opts=ResourceOptions(
                parent=self,
                providers=[aws_provider],
                depends_on=[vpc],
            ),
        )

        private_subnets = []
        public_subnets = []
        cluster_deps: List[Input[Resource]] = [vpc]
        index = 0
        for zone in nodepool_zones:  # type: ignore
            public_subnet = aws.ec2.Subnet(
                f"pvn-k8s-subnet-public-{name}-{zone}",
                availability_zone=zone,
                cidr_block=SUBNET_CIDRS[index],
                vpc_id=vpc.id,
                opts=ResourceOptions(
                    parent=self,
                    providers=[aws_provider],
                    depends_on=[vpc],
                ),
                map_public_ip_on_launch=True,
            )
            index += 1
            public_subnets.append(public_subnet)

            private_subnet = aws.ec2.Subnet(
                f"pvn-k8s-subnet-private-{name}-{zone}",
                availability_zone=zone,
                cidr_block=SUBNET_CIDRS[index],
                vpc_id=vpc.id,
                opts=ResourceOptions(
                    parent=self,
                    providers=[aws_provider],
                    depends_on=[vpc],
                ),
            )
            index += 1
            private_subnets.append(private_subnet)

            eip = aws.ec2.Eip(
                f"pvn-eip-{name}-{zone}",
                vpc=True,
                opts=ResourceOptions(
                    parent=self,
                    providers=[aws_provider],
                ),
            )

            nat_gateway = aws.ec2.NatGateway(
                f"pvn-ngw-{name}-{zone}",
                allocation_id=eip.id,
                connectivity_type="public",
                subnet_id=public_subnet.id,
                opts=ResourceOptions(
                    parent=self,
                    providers=[aws_provider],
                    depends_on=[public_subnet, eip, igw],
                    delete_before_replace=True,  # TODO: Remove
                ),
            )

            natgw_route_table = aws.ec2.RouteTable(
                f"pvn-ngw-route-{name}-{zone}",
                vpc_id=vpc.id,
                routes=[
                    aws.ec2.RouteTableRouteArgs(
                        cidr_block="0.0.0.0/0",
                        nat_gateway_id=nat_gateway.id,
                    ),
                ],
                opts=ResourceOptions(
                    parent=self,
                    providers=[aws_provider],
                    depends_on=[nat_gateway],
                ),
            )

            natgw_route_assoc = aws.ec2.RouteTableAssociation(
                f"pvn-ngw-rt-assoc-{name}-{zone}",
                subnet_id=private_subnet.id,
                route_table_id=natgw_route_table.id,
                opts=ResourceOptions(
                    parent=self,
                    providers=[aws_provider],
                    depends_on=[natgw_route_table, private_subnet],
                ),
            )

            public_route_table = aws.ec2.RouteTable(
                f"pvn-igw-route-{name}-{zone}",
                vpc_id=vpc.id,
                routes=[
                    aws.ec2.RouteTableRouteArgs(
                        cidr_block="0.0.0.0/0",
                        gateway_id=igw.id,
                    ),
                ],
                opts=ResourceOptions(
                    parent=self,
                    providers=[aws_provider],
                    depends_on=[igw],
                ),
            )

            public_route_table_assoc = aws.ec2.RouteTableAssociation(
                f"pvn-igw-rt-assoc-{name}-{zone}",
                subnet_id=public_subnet.id,
                route_table_id=public_route_table.id,
                opts=ResourceOptions(
                    parent=self,
                    providers=[aws_provider],
                    depends_on=[public_route_table, public_subnet],
                ),
            )

            cluster_deps.append(public_subnet)
            cluster_deps.append(private_subnet)
            cluster_deps.append(natgw_route_assoc)
            cluster_deps.append(public_route_table_assoc)

        role_mappings: List[eks.RoleMappingArgs] = []

        if account_id:
            # Give full admin access to anyone who can access this sub-account.
            # TODO: In the future, we should make this role configurable.
            role_mappings.append(
                eks.RoleMappingArgs(
                    groups=["system:masters"],
                    role_arn=f"arn:aws:iam::{account_id}:role/OrganizationAccountAccessRole",
                    username="root-access",
                )
            )

        eks_cluster = eks.Cluster(
            cluster_name,
            instance_type=instance_type,
            desired_capacity=node_count_per_zone,
            node_associate_public_ip_address=False,
            endpoint_private_access=False,
            endpoint_public_access=True,
            vpc_id=vpc.id,
            private_subnet_ids=[subnet.id for subnet in private_subnets],
            public_subnet_ids=[subnet.id for subnet in public_subnets],
            role_mappings=role_mappings,
            provider_credential_opts=eks.KubeconfigOptionsArgs(
                role_arn=assume_role_arn,
            )
            if assume_role_arn
            else None,
            opts=ResourceOptions(
                parent=self,
                providers=[aws_provider],
                depends_on=cluster_deps,
            ),
        )

        self.kubeconfig = eks_cluster.kubeconfig

        k8s_provider = k8s.Provider(
            "k8s-cluster",
            kubeconfig=self.kubeconfig,
            opts=ResourceOptions(parent=self, depends_on=[eks_cluster]),
        )

        self.cert_manager = CertManager(
            "cert-manager",
            opts=ResourceOptions(
                parent=self,
                providers=[aws_provider, k8s_provider],
                depends_on=[eks_cluster],
            ),
        )

        self.istio = Istio(
            "istio",
            opts=ResourceOptions(
                parent=self,
                providers=[aws_provider, k8s_provider],
                depends_on=[eks_cluster],
            ),
        )

        self.flagger = Flagger(
            "flagger",
            opts=ResourceOptions(
                parent=self,
                providers=[aws_provider, k8s_provider],
                depends_on=[eks_cluster, self.istio],
            ),
        )

        self.k8s_endpoint = eks_cluster.eks_cluster.endpoint

        outputs = {
            "k8s_endpoint": self.k8s_endpoint,
            "istio": self.istio,
            "cert_manager": self.cert_manager,
            "flagger": self.flagger,
        }

        if prodvana_managed:
            self.svc_accounts = ProdvanaServiceAccounts(
                "service-accounts",
                k8s_provider,
                opts=ResourceOptions(
                    parent=self,
                    providers=[k8s_provider],
                    depends_on=[eks_cluster],
                ),
            )

            self.prodvana_service_account_name = (
                self.svc_accounts.prodvana_service_account_name
            )
            self.prodvana_service_account_token = (
                self.svc_accounts.prodvana_service_account_token
            )
            self.prodvana_service_account_ca_crt = (
                self.svc_accounts.prodvana_service_account_ca_crt
            )

            outputs.update(
                {
                    "prodvana_service_account_name": self.prodvana_service_account_name,
                    "prodvana_service_account_token": self.prodvana_service_account_token,
                    "prodvana_service_account_ca_crt": self.prodvana_service_account_ca_crt,
                }
            )

        self.register_outputs(outputs)
