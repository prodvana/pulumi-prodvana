import textwrap
from typing import Mapping, Optional, Sequence

import pulumi_kubernetes as k8s
from pulumi import ComponentResource, Input, InvokeOptions, Output, ResourceOptions
from pulumi_gcp import organizations, projects, serviceaccount
from pulumi_gcp.container import (
    Cluster,
    ClusterIpAllocationPolicyArgs,
    ClusterPrivateClusterConfigArgs,
    NodePool,
    NodePoolNodeConfigArgs,
)

from pulumi_prodvana.network import VPC
from pulumi_prodvana.service_accounts import ProdvanaServiceAccounts

# see: https://cloud.google.com/kubernetes-engine/docs/how-to/hardening-your-cluster#use_least_privilege_sa
NODE_SA_ROLES = [
    "roles/monitoring.viewer",
    "roles/monitoring.metricWriter",
    "roles/logging.logWriter",
    "roles/stackdriver.resourceMetadata.writer",
]


class GKECluster(ComponentResource):
    def __init__(
        self,
        name: str,
        project: Input[str],
        region: Input[str],
        nodepool_zones: Input[Sequence[str]],
        node_count_per_zone: Input[int],
        instance_type: Input[str],
        vpc: VPC,
        gcp_credentials: Optional[Input[str]],
        install_prodvana_service_account: bool = False,
        cluster_id: Optional[str] = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        opts = ResourceOptions.merge(opts, ResourceOptions(depends_on=[vpc]))
        super().__init__("pvn-cluster:k8s:GKECluster", name, None, opts)

        self.gcp_credentials = gcp_credentials
        self.project = project
        self.region = region

        # create a default node Service Account
        # account id has a max length of 30, so truncate down if needed
        # (must match this regex: ^[a-z](?:[-a-z0-9]{4,28}[a-z0-9])$ )
        account_id = f"{name}"[:30]
        self.node_svc_account = serviceaccount.Account(
            f"{name}-node-svc-account",
            account_id=account_id,
            display_name=f"{name} GKE Node Service Account",
            project=project,
            opts=ResourceOptions(parent=self),
        )

        self.client_config = organizations.get_client_config(InvokeOptions(parent=self))

        self.gke_cluster = Cluster(
            f"{name}-gke",
            # HACK(mike): this pushes the problem up... but gke cluster names can be max 40 characters
            name=cluster_id[:40] if cluster_id is not None else f"{name}"[:40],
            location=region,
            remove_default_node_pool=True,
            initial_node_count=1,
            node_locations=nodepool_zones,
            private_cluster_config=ClusterPrivateClusterConfigArgs(
                enable_private_endpoint=False,
                enable_private_nodes=True,
                master_ipv4_cidr_block="172.16.0.16/28",
            ),
            network=vpc.network.name,
            subnetwork=vpc.subnet.name,
            ip_allocation_policy=ClusterIpAllocationPolicyArgs(
                cluster_secondary_range_name="pods",
                services_secondary_range_name="services",
            ),
            project=project,
            # TODO(mike): re-enable workload identity
            # workload_identity_config=ClusterWorkloadIdentityConfigArgs(
            #     # see: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity
            #     workload_pool=Output.concat(project, ".svc.id.goog"),
            # ),
            opts=ResourceOptions(parent=self),
        )

        # Bind the minimal required GCP IAM roles to the node SA
        for role in NODE_SA_ROLES:
            projects.IAMMember(
                f"{name}-{role}-binding",
                member=Output.concat("serviceAccount:", self.node_svc_account.email),
                project=project,
                role=role,
                opts=ResourceOptions(parent=self),
            )

        # Create a nodepool with specified number of nodes in each zone
        self.nodepool = NodePool(
            f"{name}-nodepool",
            # HACK(mike): this pushes the problem up... but nodepool names can be max 40 characters
            name=cluster_id[:40] if cluster_id is not None else f"{name}"[:40],
            location=region,
            node_locations=nodepool_zones,
            cluster=self.gke_cluster.name,
            node_config=NodePoolNodeConfigArgs(
                machine_type=instance_type,
                service_account=self.node_svc_account.email,
                # specify this tag so we can use it in firewall rules
                # elsewhere. gke will generate a default one but it's hard to
                # query for it.
                tags=[Output.concat(self.gke_cluster.name, "-nodes")],
                # NOTE: The cluster needs at least `storage-ro` to read from
                # Artifact Registry. Yes, GCP does say oauth_scopes are
                # deprecated, and to use IAM roles. This for some reason does
                # NOT apply to Artifact Registry. `cloud-platform` is probably
                # overly broad, but I expect other gotchas like this with other
                # services we want to talk to, so we can figure out de-scoping
                # this later if needed. I believe the IAM roles are still
                # needed in addition, so this does not give broad access to the
                # cluster by itself.
                oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            ),
            node_count=node_count_per_zone,
            project=project,
            opts=ResourceOptions(parent=self),
        )

        self.endpoint = self.gke_cluster.endpoint

        outputs = {
            "project": self.project,
            "region": self.region,
            "gke_cluster": self.gke_cluster,
            "node_svc_account": self.node_svc_account,
            "nodepool": self.nodepool,
            "endpoint": self.endpoint,
        }

        if install_prodvana_service_account:
            k8s_provider = k8s.Provider("k8s-cluster", kubeconfig=self.kubeconfig)
            self.svc_accounts = ProdvanaServiceAccounts(
                "service-accounts",
                k8s_provider,
                opts=ResourceOptions(
                    parent=self,
                    providers=[k8s_provider],
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

    @property
    def kubeconfig(self) -> Output[str]:
        # TODO(naphat) the use of access_token here causes the k8s provider to be recreated each time.
        # We need a way to communicate to pulumi that that token should not be considered part of
        # the k8s provider object hash, or just stop talking to k8s from pulumi entirely.
        def gen_kubeconfig(
            name: str,
            endpoint: str,
            master_auth: Mapping[str, str],
            region: str,
            project: str,
            gcp_credentials: Optional[str],
        ):
            identifier = f"{project}_{region}_{name}"
            return textwrap.dedent(
                f"""\
            apiVersion: v1
            clusters:
            - cluster:
                certificate-authority-data: {master_auth['cluster_ca_certificate']}
                server: https://{endpoint}
              name: {identifier}
            contexts:
            - context:
                cluster: {identifier}
                user: {identifier}
              name: {identifier}
            current-context: {identifier}
            kind: Config
            preferences: {{}}
            users:
            - name: {identifier}
              user:
                exec:
                  apiVersion: client.authentication.k8s.io/v1beta1
                  command: gke-gcloud-auth-plugin
                  installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
                    go/gke-kubectl-exec-auth
                  provideClusterInfo: true
                  env:
                  - name: GOOGLE_CREDENTIALS
                    value: {gcp_credentials or ""}
                """
            )

        k8s_info = Output.all(
            self.gke_cluster.name,
            self.gke_cluster.endpoint,
            self.gke_cluster.master_auth,
            self.region,
            self.project,
            self.gcp_credentials,
        )
        kubeconfig = k8s_info.apply(lambda info: gen_kubeconfig(*info))
        return Output.secret(kubeconfig)
