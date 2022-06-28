import base64
from typing import Optional

import pulumi_kubernetes as k8s
from pulumi import (
    ROOT_STACK_RESOURCE,
    Alias,
    ComponentResource,
    Output,
    ResourceOptions,
)


class ProdvanaServiceAccounts(ComponentResource):
    def __init__(
        self,
        name: str,
        k8s_provider: k8s.Provider,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__("pvn-cluster:k8s:ServiceAccounts", name, None, opts)

        # Install Prodvana management user so managing cluster can connect
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
