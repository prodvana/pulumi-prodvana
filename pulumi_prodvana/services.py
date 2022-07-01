import base64
import os
from typing import Optional

import pulumi_kubernetes as k8s
from pulumi import ComponentResource, FileAsset, ResourceOptions
from pulumi_kubernetes.apiextensions import CustomResource
from pulumi_kubernetes.core.v1 import Namespace, Secret
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs


class CertManager(ComponentResource):
    def __init__(
        self,
        name: str,
        cluster: ComponentResource,
        opts: Optional[ResourceOptions] = None,
    ):
        opts = ResourceOptions.merge(opts, ResourceOptions(depends_on=[cluster]))
        super().__init__("pvn-cluster:services:CertManager", name, None, opts)

        # install base cert-manager to support CA cer issuers etc.
        self.cert_manager_helm = Release(
            f"{name}-cm-release",
            ReleaseArgs(
                chart="cert-manager",
                repository_opts=RepositoryOptsArgs(
                    repo="https://charts.jetstack.io",
                ),
                namespace="cert-manager",
                create_namespace=True,
                version="1.7.1",
                # see: https://github.com/cert-manager/cert-manager/blob/v1.7.1/deploy/charts/cert-manager/values.yaml
                values={
                    "global": {
                        "replicaCount": 2,
                    },
                    "installCRDs": True,
                },
            ),
            opts=ResourceOptions(parent=self),
        )

        self.selfsigned_issuer = CustomResource(
            "self-signed-issuer",
            api_version="cert-manager.io/v1",
            kind="ClusterIssuer",
            metadata=ObjectMetaArgs(
                name="selfsigned-issuer",
            ),
            spec={
                "selfSigned": {},
            },
            opts=ResourceOptions(parent=self, depends_on=[self.cert_manager_helm]),
        )

        self.namespace = self.cert_manager_helm.namespace
        self.register_outputs(
            {
                "cert_manager_helm": self.cert_manager_helm,
                "namespace": self.namespace,
                "selfsigned_issuer": self.selfsigned_issuer,
            }
        )


class Linkerd(ComponentResource):
    def __init__(
        self,
        name: str,
        cert_mgr: CertManager,
        opts: Optional[ResourceOptions] = None,
    ):
        opts = ResourceOptions.merge(opts, ResourceOptions(depends_on=[cert_mgr]))
        super().__init__("pvn-cluster:services:Linkerd", name, None, opts)

        # create the linkerd namespace
        linkerd_ns = Namespace(
            "linkerd",
            metadata=ObjectMetaArgs(
                name="linkerd",
            ),
            opts=ResourceOptions(parent=self),
        )

        # Linkerd manages mTLS, but needs a Trust Anchor Certificate and an
        # Intermediate Issuer Certificate.
        #  Trust Anchor Cert - used to issue new Issuer certs
        #  Issuer Cert       - used to generate mTLS certs for linkerd proxies
        # Adapted from:
        # https://linkerd.io/2.11/tasks/automatically-rotating-control-plane-tls-credentials/
        #

        # create an empty secret so we have a pulumi reference to it, then
        # below the Certificate will populate it with the certificate data.
        trust_anchor_secret = Secret(
            "linkerd-trust-anchor-secret",
            metadata=ObjectMetaArgs(
                name="linkerd-trust-anchor",
                namespace=linkerd_ns.metadata["name"],
            ),
            opts=ResourceOptions(parent=self),
        )

        # First create the Trust Anchor Certificate using the GoogleCASIssuer
        trust_anchor_cert = CustomResource(
            "linkerd-trust-anchor-cert",
            api_version="cert-manager.io/v1",
            kind="Certificate",
            metadata=ObjectMetaArgs(
                name="linkerd-trust-anchor",
                namespace=linkerd_ns.metadata["name"],
            ),
            spec={
                "secretName": trust_anchor_secret.metadata.name,
                "commonName": "root.linkerd.cluster.local",
                "dnsNames": ["root.linkerd.cluster.local"],
                "duration": "2160h",  # 90d
                "renewBefore": "240h",  # 10d
                "issuerRef": {
                    "group": "cert-manager.io",
                    "kind": "ClusterIssuer",
                    "name": cert_mgr.selfsigned_issuer.metadata["name"],  # type: ignore
                },
                "privateKey": {"algorithm": "ECDSA", "size": 256},
                "isCA": True,
            },
            opts=ResourceOptions(parent=self),
        )
        # Create an Issuer so we can use the generated Trust Anchor Cert as a CA
        trust_anchor_issuer = CustomResource(
            "linkerd-trust-anchor-issuer",
            api_version="cert-manager.io/v1",
            kind="Issuer",
            metadata=ObjectMetaArgs(
                name="linkerd-trust-anchor",
                namespace=linkerd_ns.metadata["name"],
            ),
            spec={
                "ca": {
                    "secretName": trust_anchor_secret.metadata.name,
                },
            },
            opts=ResourceOptions(parent=self, depends_on=[trust_anchor_cert]),
        )

        # Next use the Trust Anchor cert to generate the intermediate CA Linkerd
        # will use to issue mTLS certs
        id_issuer_cert = CustomResource(
            "linkerd-issuer",
            api_version="cert-manager.io/v1",
            kind="Certificate",
            metadata=ObjectMetaArgs(
                name="linkerd-identity-issuer",
                namespace=linkerd_ns.metadata["name"],
            ),
            spec={
                "secretName": "linkerd-identity-issuer",
                "duration": "48h",
                "renewBefore": "25h",
                "issuerRef": {
                    "name": trust_anchor_issuer.metadata["name"],  # type: ignore
                    "kind": "Issuer",
                },
                "commonName": "identity.linkerd.cluster.local",
                "dnsNames": ["identity.linkerd.cluster.local"],
                "isCA": True,
                "privateKey": {"algorithm": "ECDSA"},
                "usages": [
                    "cert sign",
                    "crl sign",
                    "server auth",
                    "client auth",
                ],
            },
            opts=ResourceOptions(parent=self),
        )

        # fetch the Secret so we can get the `ca.crt` and pass it to Linkerd's
        # helm values
        fetched_trust_anchor = Secret.get(
            "trust-anchor-secret-fetch",
            trust_anchor_secret.id,
            opts=ResourceOptions(parent=self, depends_on=[trust_anchor_cert]),
        )

        # k8s stores Secret values base64 encoded, so decode before passing on
        trust_anchor_pem = fetched_trust_anchor.data.apply(
            lambda data: base64.b64decode(data["ca.crt"]).decode("utf-8")
        )

        libdir = os.path.dirname(__file__)

        linkerd_helm = Release(
            "helm-linkerd",
            ReleaseArgs(
                chart="linkerd2",
                repository_opts=RepositoryOptsArgs(
                    repo="https://helm.linkerd.io/stable",
                ),
                namespace="linkerd",
                create_namespace=False,
                version="2.11.1",
                value_yaml_files=[
                    FileAsset(os.path.join(libdir, "linkerd2-values-ha.yaml"))
                ],
                values={
                    "identityTrustAnchorsPEM": trust_anchor_pem,
                    "identity": {
                        "issuer": {"scheme": "kubernetes.io/tls"},
                    },
                    "installNamespace": False,
                },
            ),
            opts=ResourceOptions(parent=self, depends_on=[id_issuer_cert]),
        )

        Release(
            "helm-linkerd-viz",
            ReleaseArgs(
                chart="linkerd-viz",
                repository_opts=RepositoryOptsArgs(
                    repo="https://helm.linkerd.io/stable",
                ),
                version="2.11.1",
                value_yaml_files=[
                    FileAsset(os.path.join(libdir, "linkerd-viz-values-ha.yaml"))
                ],
                values={
                    "installNamespace": True,
                },
            ),
            opts=ResourceOptions(parent=self, depends_on=[linkerd_helm]),
        )


class Istio(ComponentResource):
    def __init__(
        self,
        name: str,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__("pvn-cluster:services:Istio", name, None, opts)
        # create the istio namespace
        Namespace(
            "istio-ns",
            metadata=ObjectMetaArgs(
                name="istio-system",
            ),
            opts=ResourceOptions(parent=self),
        )

        repo_opts = k8s.helm.v3.RepositoryOptsArgs(
            repo="https://istio-release.storage.googleapis.com/charts",
        )
        version = "1.14.1"

        # instlal base istio components
        istio_base = k8s.helm.v3.Release(
            "helm-istio-base",
            k8s.helm.v3.ReleaseArgs(
                chart="base",
                repository_opts=repo_opts,
                version=version,
                namespace="istio-system",
            ),
            opts=ResourceOptions(parent=self),
        )

        # install istio discovery control plane
        k8s.helm.v3.Release(
            "helm-istiod",
            k8s.helm.v3.ReleaseArgs(
                chart="istiod",
                repository_opts=repo_opts,
                version=version,
                namespace="istio-system",
                values={
                    "pilot": {
                        "env": {
                            "PILOT_SCOPE_GATEWAY_TO_NAMESPACE": "true",
                        }
                    }
                },
            ),
            opts=ResourceOptions(parent=self, depends_on=[istio_base]),
        )


FLAGGER_CHART_VERSION = "1.20.0"


class Flagger(ComponentResource):
    def __init__(
        self,
        name: str,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__("pvn-cluster:services:Flagger", name, None, opts)

        # NOTE: crds must be installed first
        flagger_crd = k8s.yaml.ConfigFile(
            f"{name}-flagger-crd",
            file=f"https://raw.githubusercontent.com/fluxcd/flagger/v{FLAGGER_CHART_VERSION}/charts/flagger/crds/crd.yaml",
            opts=ResourceOptions(parent=self, providers=opts.providers),
        )

        k8s.helm.v3.Release(
            "helm-flagger",
            k8s.helm.v3.ReleaseArgs(
                chart="flagger",
                repository_opts=k8s.helm.v3.RepositoryOptsArgs(
                    repo="https://flagger.app",
                ),
                version=FLAGGER_CHART_VERSION,
                # flagger docs say to install in the istio-system namespace
                namespace="istio-system",
                values={
                    "meshProvider": "istio",
                    "metricsServer": "http://prometheus.istio-sytem:9090",
                },
            ),
            opts=ResourceOptions(parent=self, depends_on=[flagger_crd]),
        )
