from typing import Optional, Sequence

import pulumi_kubernetes as k8s
from pulumi import ComponentResource, Input, ResourceOptions

from pulumi_prodvana.k8s import GKECluster
from pulumi_prodvana.network import VPC
from pulumi_prodvana.services import CertManager, Flagger, Linkerd


class Cluster(ComponentResource):
    def __init__(
        self,
        name: str,
        project: Input[str],
        region: Input[str],
        nodepool_zones: Input[Sequence[str]],
        node_count_per_zone: Input[int],
        instance_type: Input[str],
        prodvana_managed: bool = True,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__("pvn-cluster:index:Cluster", name, None, opts)

        self.project = project
        self.region = region

        self.vpc = VPC(
            f"pnet-{name}",
            project=project,
            region=region,
            opts=ResourceOptions(parent=self),
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
            opts=ResourceOptions(parent=self, depends_on=[self.vpc]),
        )

        k8s_provider = k8s.Provider(
            "k8s-cluster",
            kubeconfig=self.k8s_cluster.kubeconfig,
            opts=ResourceOptions(parent=self, depends_on=[self.k8s_cluster]),
        )
        self.cert_mgr = CertManager(
            "cert-manager",
            self.k8s_cluster,
            opts=ResourceOptions(
                parent=self, providers=[k8s_provider], depends_on=[self.k8s_cluster]
            ),
        )

        self.linkerd = Linkerd(
            "linkerd",
            self.k8s_cluster,
            self.vpc,
            self.cert_mgr,
            opts=ResourceOptions(
                parent=self, providers=[k8s_provider], depends_on=[self.k8s_cluster]
            ),
        )

        self.flagger = Flagger(
            "flagger",
            opts=ResourceOptions(
                parent=self,
                providers=[k8s_provider],
                depends_on=[self.k8s_cluster, self.linkerd],
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
            "cert_mgr": self.cert_mgr,
            "linkerd": self.linkerd,
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
