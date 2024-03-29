# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
    'get_application_output',
]

@pulumi.output_type
class GetApplicationResult:
    """
    A collection of values returned by getApplication.
    """
    def __init__(__self__, id=None, name=None, version=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Application identifier
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Application name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Current application version
        """
        return pulumi.get(self, "version")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            id=self.id,
            name=self.name,
            version=self.version)


def get_application(name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    Prodvana Application

    ## Example Usage

    ```python
    import pulumi
    import pulumi_prodvana as prodvana

    example = prodvana.get_application(name="my-app")
    ```


    :param str name: Application name
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('prodvana:index/getApplication:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        version=pulumi.get(__ret__, 'version'))


@_utilities.lift_output_func(get_application)
def get_application_output(name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplicationResult]:
    """
    Prodvana Application

    ## Example Usage

    ```python
    import pulumi
    import pulumi_prodvana as prodvana

    example = prodvana.get_application(name="my-app")
    ```


    :param str name: Application name
    """
    ...
