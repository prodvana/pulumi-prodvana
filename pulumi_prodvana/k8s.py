import base64
import textwrap
from typing import Any, Mapping, Optional, Sequence

import pulumi_kubernetes as k8s
from pulumi import (
    ROOT_STACK_RESOURCE,
    Alias,
    ComponentResource,
    Input,
    Output,
    ResourceOptions,
)
from pulumi_gcp import projects, serviceaccount
from pulumi_gcp.container import (
    Cluster,
    ClusterIpAllocationPolicyArgs,
    ClusterPrivateClusterConfigArgs,
    NodePool,
    NodePoolNodeConfigArgs,
)

from pulumi_prodvana.network import VPC

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
        install_prodvana_service_account: bool = False,
        cluster_id: Optional[str] = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        opts = ResourceOptions.merge(opts, ResourceOptions(depends_on=[vpc]))
        super().__init__("pvn-cluster:k8s:GKECluster", name, None, opts)

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
            addl_outs = self.install_prodvana_service_account()
            outputs.update(addl_outs)

        self.register_outputs(outputs)

    # Install Prodvana management user so managing cluster can connect
    def install_prodvana_service_account(self) -> Mapping[str, Any]:
        k8s_provider = k8s.Provider("k8s-cluster", kubeconfig=self.kubeconfig)
        pvn_svc_account = k8s.core.v1.ServiceAccount(
            "prodvana-mgmt-sa",
            metadata=k8s.meta.v1.ObjectMetaArgs(
                name="prodvana",
                namespace="default",
            ),
            opts=ResourceOptions(
                providers=[k8s_provider],
                aliases=[Alias(parent=ROOT_STACK_RESOURCE)],
                parent=self,
            ),
        )
        role_binding = k8s.rbac.v1.ClusterRoleBinding(
            "prodvana-mgmt-sa-role-binding",
            metadata=k8s.meta.v1.ObjectMetaArgs(
                name="prodvana-cluster-access",
            ),
            subjects=[
                k8s.rbac.v1.SubjectArgs(
                    kind="ServiceAccount",
                    name=pvn_svc_account.metadata.name,
                    namespace=pvn_svc_account.metadata.namespace,
                ),
            ],
            role_ref=k8s.rbac.v1.RoleRefArgs(
                api_group="rbac.authorization.k8s.io",
                kind="ClusterRole",
                name="cluster-admin",
            ),
            opts=ResourceOptions(
                providers=[k8s_provider],
                aliases=[Alias(parent=ROOT_STACK_RESOURCE)],
                parent=self,
            ),
        )

        fetched_svc_account = k8s.core.v1.ServiceAccount.get(
            "prodvana-mgmt-sa-fetched",
            id=pvn_svc_account.id,
            opts=ResourceOptions(
                providers=[k8s_provider],
                depends_on=[pvn_svc_account, role_binding],
                parent=self,
                aliases=[Alias(parent=ROOT_STACK_RESOURCE)],
            ),
        )

        token_secrets = fetched_svc_account.secrets.apply(
            lambda secrets: [
                secret
                for secret in secrets
                if secret.name.startswith("prodvana-token-")
            ]
        )
        token_secret = token_secrets[0]

        fetched_secret = k8s.core.v1.Secret.get(
            "prodvana-mgmt-sa-token-fetched",
            id=token_secret["name"],
            opts=ResourceOptions(
                providers=[k8s_provider],
                depends_on=[pvn_svc_account, role_binding, fetched_svc_account],
                parent=self,
                aliases=[Alias(parent=ROOT_STACK_RESOURCE)],
            ),
        )

        self.prodvana_service_account_name = pvn_svc_account.metadata.name
        token = fetched_secret.data["token"].apply(
            lambda secret: base64.standard_b64decode(secret).decode("utf-8")
        )
        self.prodvana_service_account_token = Output.secret(token)
        ca_crt = fetched_secret.data["ca.crt"].apply(
            lambda secret: base64.standard_b64decode(secret).decode("utf-8")
        )
        self.prodvana_service_account_ca_crt = Output.secret(ca_crt)

        return {
            "prodvana_service_account_name": self.prodvana_service_account_name,
            "prodvana_service_account_token": self.prodvana_service_account_token,
            "prodvana_service_account_ca_crt": self.prodvana_service_account_ca_crt,
        }

    @property
    def kubeconfig(self) -> Output[str]:
        def gen_kubeconfig(
            name: str,
            endpoint: str,
            master_auth: Mapping[str, str],
            region: str,
            project: str,
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
                auth-provider:
                  config:
                    cmd-args: config config-helper --format=json
                    cmd-path: gcloud
                    expiry-key: '{{.credential.token_expiry}}'
                    token-key: '{{.credential.access_token}}'
                  name: gcp
                """
            )

        k8s_info = Output.all(
            self.gke_cluster.name,
            self.gke_cluster.endpoint,
            self.gke_cluster.master_auth,
            self.region,
            self.project,
        )
        kubeconfig = k8s_info.apply(lambda info: gen_kubeconfig(*info))
        return Output.secret(kubeconfig)
