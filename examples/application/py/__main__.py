"""A Python Pulumi program"""

import pulumi
import pulumi_prodvana as prodvana


app = prodvana.Application("my-test-app-py", name="my-test-app-py")