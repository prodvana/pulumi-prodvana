from typing import Optional

import pulumi_gcp as gcp
import pulumi_random as random
from pulumi import Input, Output, ResourceOptions


def create_project(
    project_name: Input[str],
    org_id: Input[str],
    billing_account: Input[str],
    verbatim_id: bool = False,
    opts: Optional[ResourceOptions] = None,
) -> gcp.organizations.Project:
    if verbatim_id:
        project_id = project_name
    else:
        random_id = random.RandomId(f"{project_name}-random-id", byte_length=2)
        project_id = Output.concat(f"{project_name}-", random_id.dec)

    return gcp.organizations.Project(
        f"{project_name}-project",
        name=project_name,
        project_id=project_id,
        org_id=org_id,
        billing_account=billing_account,
        opts=opts,
    )
