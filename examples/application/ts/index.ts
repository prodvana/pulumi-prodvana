import * as pulumi from "@pulumi/pulumi";
import * as prodvana from "@prodvana/pulumi-prodvana"

const app = new prodvana.Application("my-test-app-ts", {
   name: "my-test-app-ts",
})