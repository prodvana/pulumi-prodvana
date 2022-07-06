from typing import Optional, Sequence

import pulumi_aws as aws
import pulumi_eks as eks

import pulumi_kubernetes as k8s
from pulumi import ComponentResource, Input, ResourceOptions

from pulumi_prodvana.service_accounts import ProdvanaServiceAccounts
from pulumi_prodvana.services import CertManager, Flagger, Istio


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

        eks_cluster = eks.Cluster(
            cluster_name,
            instance_type=instance_type,
            desired_capacity=node_count_per_zone,
            provider_credential_opts=eks.KubeconfigOptionsArgs(
                role_arn=assume_role_arn,
            )
            if assume_role_arn
            else None,
            opts=ResourceOptions(
                parent=self,
                providers=[aws_provider],
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
                depends_on=[self.k8s_cluster],
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
