from typing import Optional

from pulumi import ComponentResource, Input, ResourceOptions
from pulumi_gcp.compute import (
    Network,
    Router,
    RouterNat,
    Subnetwork,
    SubnetworkSecondaryIpRangeArgs,
)

PODS_CIDR = "10.1.0.0/16"
SERVICES_CIDR = "10.2.0.0/20"


class VPC(ComponentResource):
    def __init__(
        self,
        name: str,
        project: Input[str],
        region: Input[str],
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__("pvn-cluster:network:VPC", name, None, opts)
        # Create customer mgmt cluster VPC
        self.network = Network(
            f"{name}-vpc",
            auto_create_subnetworks=False,
            project=project,
            opts=ResourceOptions(parent=self),
        )

        # Create a subnet in the specified region
        self.subnet = Subnetwork(
            f"{name}-subnet",
            project=project,
            network=self.network.id,
            region=region,
            ip_cidr_range="10.0.0.0/20",
            private_ip_google_access=True,
            secondary_ip_ranges=[
                SubnetworkSecondaryIpRangeArgs(
                    range_name="pods",
                    ip_cidr_range=PODS_CIDR,
                ),
                SubnetworkSecondaryIpRangeArgs(
                    range_name="services",
                    ip_cidr_range=SERVICES_CIDR,
                ),
            ],
            opts=ResourceOptions(parent=self),
        )

        # Router and RouterNat needed to allow GKE pods to initiate connections
        # to the public internet since the nodes only have private IPs.
        self.router = Router(
            f"{name}-router",
            project=project,
            region=self.subnet.region,
            network=self.network.id,
            opts=ResourceOptions(parent=self),
        )

        self.nat = RouterNat(
            f"{name}-nat",
            project=project,
            router=self.router.name,
            region=self.router.region,
            nat_ip_allocate_option="AUTO_ONLY",
            source_subnetwork_ip_ranges_to_nat="ALL_SUBNETWORKS_ALL_IP_RANGES",
            opts=ResourceOptions(parent=self),
        )
