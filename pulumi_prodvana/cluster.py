from typing import Optional, Sequence

import pulumi_gcp as gcp
import pulumi_kubernetes as k8s
from pulumi import ComponentResource, Input, ResourceOptions

from pulumi_prodvana.k8s import GKECluster
from pulumi_prodvana.network import VPC
from pulumi_prodvana.services import Flagger, Istio


class Cluster(ComponentResource):
    def __init__(
        self,
        name: str,
        project: Input[str],
        region: Input[str],
        nodepool_zones: Input[Sequence[str]],
        node_count_per_zone: Input[int],
        instance_type: Input[str],
        gcp_credentials: Optional[Input[str]] = None,
        prodvana_managed: bool = True,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__("pvn-cluster:index:Cluster", name, None, opts)

        self.project = project
        self.region = region
        gcp_provider = gcp.Provider(
            "gcp",
            project=project,
            credentials=gcp_credentials,
        )

        self.vpc = VPC(
            f"pnet-{name}",
            project=project,
            region=region,
            opts=ResourceOptions(parent=self, providers=[gcp_provider]),
        )

        self.k8s_cluster = GKECluster(
            f"pvn-k8s-{name}",
            project=project,
            region=region,
            nodepool_zones=nodepool_zones,
            node_count_per_zone=node_count_per_zone,
            instance_type=instance_type,
            install_prodvana_service_account=prodvana_managed,
            vpc=self.vpc,
            opts=ResourceOptions(
                parent=self, providers=[gcp_provider], depends_on=[self.vpc]
            ),
        )

        k8s_provider = k8s.Provider(
            "k8s-cluster",
            kubeconfig=self.k8s_cluster.kubeconfig,
            opts=ResourceOptions(parent=self, depends_on=[self.k8s_cluster]),
        )

        # private clusters need some firewall setup so istio can function properly.
        # see: https://istio.io/latest/docs/setup/platform-setup/gke/
        ctrl_plane_cidr = (
            self.k8s_cluster.gke_cluster.private_cluster_config.master_ipv4_cidr_block
        )

        cluster_tag = self.k8s_cluster.nodepool.node_config.tags[0]

        gcp.compute.Firewall(
            "gke-to-istio-control-plane",
            allows=[
                gcp.compute.FirewallAllowArgs(
                    ports=["15017"],
                    protocol="tcp",
                )
            ],
            description="Allow traffic on ports 15017 for istio control-plane components",
            network=self.vpc.network.name,
            project=self.vpc.network.project,
            source_ranges=[ctrl_plane_cidr],
            target_tags=[cluster_tag],
            priority=1000,
            opts=ResourceOptions(parent=self),
        )
        self.istio = Istio(
            "istio",
            opts=ResourceOptions(
                parent=self,
                providers=[gcp_provider, k8s_provider],
                depends_on=[self.k8s_cluster],
            ),
        )

        self.flagger = Flagger(
            "flagger",
            opts=ResourceOptions(
                parent=self,
                providers=[gcp_provider, k8s_provider],
                depends_on=[self.k8s_cluster, self.istio],
            ),
        )

        # re-export fields from subcomponents to make access easier
        self.k8s_endpoint = self.k8s_cluster.endpoint
        outputs = {
            "project": self.project,
            "region": self.region,
            "vpc": self.vpc,
            "k8s_cluster": self.k8s_cluster,
            "k8s_endpoint": self.k8s_endpoint,
            "istio": self.istio,
            "flagger": self.flagger,
        }
        if prodvana_managed:
            self.prodvana_service_account_name = (
                self.k8s_cluster.prodvana_service_account_name
            )

            self.prodvana_service_account_token = (
                self.k8s_cluster.prodvana_service_account_token
            )
            self.prodvana_service_account_ca_crt = (
                self.k8s_cluster.prodvana_service_account_ca_crt
            )
            outputs.update(
                {
                    "prodvana_service_account_name": self.prodvana_service_account_name,
                    "prodvana_service_account_token": self.prodvana_service_account_token,
                    "prodvana_service_account_ca_crt": self.prodvana_service_account_ca_crt,
                }
            )
        self.register_outputs(outputs)
