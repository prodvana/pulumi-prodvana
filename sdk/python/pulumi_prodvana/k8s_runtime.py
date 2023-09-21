# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['K8sRuntimeArgs', 'K8sRuntime']

@pulumi.input_type
class K8sRuntimeArgs:
    def __init__(__self__, *,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input['K8sRuntimeLabelArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a K8sRuntime resource.
        :param pulumi.Input[Sequence[pulumi.Input['K8sRuntimeLabelArgs']]] labels: List of labels to apply to the runtime
        :param pulumi.Input[str] name: Runtime name
        """
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['K8sRuntimeLabelArgs']]]]:
        """
        List of labels to apply to the runtime
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['K8sRuntimeLabelArgs']]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Runtime name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _K8sRuntimeState:
    def __init__(__self__, *,
                 agent_api_token: Optional[pulumi.Input[str]] = None,
                 agent_args: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 agent_image: Optional[pulumi.Input[str]] = None,
                 agent_url: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input['K8sRuntimeLabelArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering K8sRuntime resources.
        :param pulumi.Input[str] agent_api_token: API Token used for linking the Kubernetes Prodvana agent
        :param pulumi.Input[Sequence[pulumi.Input[str]]] agent_args: Arguments to pass to the Kubernetes Prodvana agent container.
        :param pulumi.Input[str] agent_image: URL of the Kubernetes Prodvana agent container image.
        :param pulumi.Input[str] agent_url: URL of the Kubernetes Prodvana agent server
        :param pulumi.Input[Sequence[pulumi.Input['K8sRuntimeLabelArgs']]] labels: List of labels to apply to the runtime
        :param pulumi.Input[str] name: Runtime name
        """
        if agent_api_token is not None:
            pulumi.set(__self__, "agent_api_token", agent_api_token)
        if agent_args is not None:
            pulumi.set(__self__, "agent_args", agent_args)
        if agent_image is not None:
            pulumi.set(__self__, "agent_image", agent_image)
        if agent_url is not None:
            pulumi.set(__self__, "agent_url", agent_url)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="agentApiToken")
    def agent_api_token(self) -> Optional[pulumi.Input[str]]:
        """
        API Token used for linking the Kubernetes Prodvana agent
        """
        return pulumi.get(self, "agent_api_token")

    @agent_api_token.setter
    def agent_api_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_api_token", value)

    @property
    @pulumi.getter(name="agentArgs")
    def agent_args(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Arguments to pass to the Kubernetes Prodvana agent container.
        """
        return pulumi.get(self, "agent_args")

    @agent_args.setter
    def agent_args(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "agent_args", value)

    @property
    @pulumi.getter(name="agentImage")
    def agent_image(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the Kubernetes Prodvana agent container image.
        """
        return pulumi.get(self, "agent_image")

    @agent_image.setter
    def agent_image(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_image", value)

    @property
    @pulumi.getter(name="agentUrl")
    def agent_url(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the Kubernetes Prodvana agent server
        """
        return pulumi.get(self, "agent_url")

    @agent_url.setter
    def agent_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_url", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['K8sRuntimeLabelArgs']]]]:
        """
        List of labels to apply to the runtime
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['K8sRuntimeLabelArgs']]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Runtime name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class K8sRuntime(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['K8sRuntimeLabelArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource allows you to manage a Prodvana Kubernetes [Runtime](https://docs.prodvana.io/docs/prodvana-concepts#runtime). You are responsible for managing the agent lifetime. Also see `ManagedK8sRuntime`.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_prodvana as prodvana

        example = prodvana.K8sRuntime("example", labels=[
            prodvana.K8sRuntimeLabelArgs(
                label="env",
                value="staging",
            ),
            prodvana.K8sRuntimeLabelArgs(
                label="region",
                value="us-central1",
            ),
        ])
        ```

        ## Import

        ```sh
         $ pulumi import prodvana:index/k8sRuntime:K8sRuntime example <runtime name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['K8sRuntimeLabelArgs']]]] labels: List of labels to apply to the runtime
        :param pulumi.Input[str] name: Runtime name
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[K8sRuntimeArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource allows you to manage a Prodvana Kubernetes [Runtime](https://docs.prodvana.io/docs/prodvana-concepts#runtime). You are responsible for managing the agent lifetime. Also see `ManagedK8sRuntime`.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_prodvana as prodvana

        example = prodvana.K8sRuntime("example", labels=[
            prodvana.K8sRuntimeLabelArgs(
                label="env",
                value="staging",
            ),
            prodvana.K8sRuntimeLabelArgs(
                label="region",
                value="us-central1",
            ),
        ])
        ```

        ## Import

        ```sh
         $ pulumi import prodvana:index/k8sRuntime:K8sRuntime example <runtime name>
        ```

        :param str resource_name: The name of the resource.
        :param K8sRuntimeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(K8sRuntimeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['K8sRuntimeLabelArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = K8sRuntimeArgs.__new__(K8sRuntimeArgs)

            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            __props__.__dict__["agent_api_token"] = None
            __props__.__dict__["agent_args"] = None
            __props__.__dict__["agent_image"] = None
            __props__.__dict__["agent_url"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["agentApiToken", "agentArgs"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(K8sRuntime, __self__).__init__(
            'prodvana:index/k8sRuntime:K8sRuntime',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            agent_api_token: Optional[pulumi.Input[str]] = None,
            agent_args: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            agent_image: Optional[pulumi.Input[str]] = None,
            agent_url: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['K8sRuntimeLabelArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'K8sRuntime':
        """
        Get an existing K8sRuntime resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] agent_api_token: API Token used for linking the Kubernetes Prodvana agent
        :param pulumi.Input[Sequence[pulumi.Input[str]]] agent_args: Arguments to pass to the Kubernetes Prodvana agent container.
        :param pulumi.Input[str] agent_image: URL of the Kubernetes Prodvana agent container image.
        :param pulumi.Input[str] agent_url: URL of the Kubernetes Prodvana agent server
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['K8sRuntimeLabelArgs']]]] labels: List of labels to apply to the runtime
        :param pulumi.Input[str] name: Runtime name
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _K8sRuntimeState.__new__(_K8sRuntimeState)

        __props__.__dict__["agent_api_token"] = agent_api_token
        __props__.__dict__["agent_args"] = agent_args
        __props__.__dict__["agent_image"] = agent_image
        __props__.__dict__["agent_url"] = agent_url
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        return K8sRuntime(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentApiToken")
    def agent_api_token(self) -> pulumi.Output[str]:
        """
        API Token used for linking the Kubernetes Prodvana agent
        """
        return pulumi.get(self, "agent_api_token")

    @property
    @pulumi.getter(name="agentArgs")
    def agent_args(self) -> pulumi.Output[Sequence[str]]:
        """
        Arguments to pass to the Kubernetes Prodvana agent container.
        """
        return pulumi.get(self, "agent_args")

    @property
    @pulumi.getter(name="agentImage")
    def agent_image(self) -> pulumi.Output[str]:
        """
        URL of the Kubernetes Prodvana agent container image.
        """
        return pulumi.get(self, "agent_image")

    @property
    @pulumi.getter(name="agentUrl")
    def agent_url(self) -> pulumi.Output[str]:
        """
        URL of the Kubernetes Prodvana agent server
        """
        return pulumi.get(self, "agent_url")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Sequence['outputs.K8sRuntimeLabel']]:
        """
        List of labels to apply to the runtime
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Runtime name
        """
        return pulumi.get(self, "name")

