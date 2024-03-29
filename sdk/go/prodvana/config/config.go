// Code generated by the Pulumi Terraform Bridge (tfgen) Tool DO NOT EDIT.
// *** WARNING: Do not edit by hand unless you're certain you know what you are doing! ***

package config

import (
	"github.com/prodvana/pulumi-prodvana/sdk/go/prodvana/internal"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

var _ = internal.GetEnvOrDefault

// An API token generated with permissions to this organization.
func GetApiToken(ctx *pulumi.Context) string {
	v, err := config.Try(ctx, "prodvana:apiToken")
	if err == nil {
		return v
	}
	var value string
	if d := internal.GetEnvOrDefault(nil, nil, "PVN_API_TOKEN"); d != nil {
		value = d.(string)
	}
	return value
}

// Prodvana organization to authenticate with (you can find this in your Org's url: <org>.prodvana.io)
func GetOrgSlug(ctx *pulumi.Context) string {
	v, err := config.Try(ctx, "prodvana:orgSlug")
	if err == nil {
		return v
	}
	var value string
	if d := internal.GetEnvOrDefault(nil, nil, "PVN_ORG_SLUG"); d != nil {
		value = d.(string)
	}
	return value
}
