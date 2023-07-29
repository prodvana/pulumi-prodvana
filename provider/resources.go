// Copyright 2016-2018, Pulumi Corporation.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package prodvana

import (
	_ "embed"
	"fmt"
	"path/filepath"

	"github.com/prodvana/pulumi-prodvana/provider/pkg/version"
	"github.com/prodvana/terraform-provider-prodvana/pulumi"
	pf "github.com/pulumi/pulumi-terraform-bridge/pf/tfbridge"
	"github.com/pulumi/pulumi-terraform-bridge/v3/pkg/tfbridge"
	"github.com/pulumi/pulumi-terraform-bridge/v3/pkg/tfbridge/tokens"
	shim "github.com/pulumi/pulumi-terraform-bridge/v3/pkg/tfshim"
	"github.com/pulumi/pulumi/sdk/v3/go/common/resource"
)

// all of the token components used below.
const (
	// This variable controls the default name of the package in the package
	// registries for nodejs and python:
	mainPkg = "prodvana"
	// modules:
	mainMod = "index" // the prodvana module
)

// preConfigureCallback is called before the providerConfigure function of the underlying provider.
// It should validate that the provider can be configured, and provide actionable errors in the case
// it cannot be. Configuration variables can be read from `vars` using the `stringValue` function -
// for example `stringValue(vars, "accessKey")`.
func preConfigureCallback(vars resource.PropertyMap, c shim.ResourceConfig) error {
	return nil
}

//go:embed cmd/pulumi-resource-prodvana/bridge-metadata.json
var bridgeMetadata []byte

// Provider returns additional overlaid schema and metadata associated with the provider..
func Provider() tfbridge.ProviderInfo {
	// Instantiate the Terraform provider
	p := pf.ShimProvider(pulumi.NewProvider())

	// Create a Pulumi provider mapping
	prov := tfbridge.ProviderInfo{
		P:            p,
		Version:      version.Version,
		MetadataInfo: tfbridge.NewProviderMetadata(bridgeMetadata),
		Name: "prodvana",
		DisplayName: "Prodvana",
		Publisher: "Prodvana",
		// LogoURL is optional but useful to help identify your package in the Pulumi Registry
		// if this package is published there.
		//
		// You may host a logo on a domain you control or add an SVG logo for your package
		// in your repository and use the raw content URL for that file as your logo URL.
		LogoURL: "",
		PluginDownloadURL: "github://api.github.com/prodvana",
		Description:       "A Pulumi package for creating and managing Prodvana cloud resources.",
		// category/cloud tag helps with categorizing the package in the Pulumi Registry.
		// For all available categories, see `Keywords` in
		// https://www.pulumi.com/docs/guides/pulumi-packages/schema/#package.
		Keywords:   []string{"pulumi", "prodvana", "category/cloud", "category/infrastructure"},
		License:    "Apache-2.0",
		Homepage:   "https://prodvana.io",
		Repository: "https://github.com/prodvana/pulumi-prodvana",
		GitHubOrg: "prodvana",
		Config: map[string]*tfbridge.SchemaInfo{
			"api_token": {
				Default: &tfbridge.DefaultInfo{
					EnvVars: []string{"PVN_API_TOKEN"},
				},
			},

			"org_slug": {
				Default: &tfbridge.DefaultInfo{
					EnvVars: []string{"PVN_ORG_SLUG"},
				},
			},
		},
		PreConfigureCallback: preConfigureCallback,
		Resources:            map[string]*tfbridge.ResourceInfo{
			// "prodvana_application":         {Tok: tfbridge.MakeResource(mainPkg, mainMod, "Application")},
			// "prodvana_k8s_runtime":         {Tok: tfbridge.MakeResource(mainPkg, mainMod, "K8sRuntime")},
			// "prodvana_managed_k8s_runtime": {Tok: tfbridge.MakeResource(mainPkg, mainMod, "ManagedK8sRuntime")},
			// "prodvana_release_channel":     {Tok: tfbridge.MakeResource(mainPkg, mainMod, "ReleaseChannel")},
			// "prodvana_runtime_link":        {Tok: tfbridge.MakeResource(mainPkg, mainMod, "RuntimeLink")},
		},
		DataSources: map[string]*tfbridge.DataSourceInfo{
			// "prodvana_application":     {Tok: tfbridge.MakeDataSource(mainPkg, mainMod, "getApplication")},
			// "prodvana_k8s_runtime":     {Tok: tfbridge.MakeDataSource(mainPkg, mainMod, "getK8sRuntime")},
			// "prodvana_release_channel": {Tok: tfbridge.MakeDataSource(mainPkg, mainMod, "getReleaseChannel")},
		},
		JavaScript: &tfbridge.JavaScriptInfo{
			PackageName: "@prodvana/pulumi-prodvana",
			// List any npm dependencies and their versions
			Dependencies: map[string]string{
				"@pulumi/pulumi": "^3.0.0",
			},
			DevDependencies: map[string]string{
				"@types/node": "^10.0.0", // so we can access strongly typed node definitions.
				"@types/mime": "^2.0.0",
			},
			// See the documentation for tfbridge.OverlayInfo for how to lay out this
			// section, or refer to the AWS provider. Delete this section if there are
			// no overlay files.
			//Overlay: &tfbridge.OverlayInfo{},
		},
		Python: &tfbridge.PythonInfo{
			// List any Python dependencies and their version ranges
			Requires: map[string]string{
				"pulumi": ">=3.0.0,<4.0.0",
			},
		},
		Golang: &tfbridge.GolangInfo{
			ImportBasePath: filepath.Join(
				fmt.Sprintf("github.com/prodvana/pulumi-%[1]s/sdk/", mainPkg),
				tfbridge.GetModuleMajorVersion(version.Version),
				"go",
				mainPkg,
			),
			GenerateResourceContainerTypes: true,
		},
		CSharp: &tfbridge.CSharpInfo{
			PackageReferences: map[string]string{
				"Pulumi": "3.*",
			},
		},
	}

	// These are new API's that you may opt to use to automatically compute resource tokens,
	// and apply auto aliasing for full backwards compatibility.
	// For more information, please reference: https://pkg.go.dev/github.com/pulumi/pulumi-terraform-bridge/v3/pkg/tfbridge#ProviderInfo.ComputeTokens
	prov.MustComputeTokens(tokens.SingleModule("prodvana_", mainMod, tokens.MakeStandard(mainPkg)))
	prov.MustApplyAutoAliases()
	prov.SetAutonaming(255, "-")

	return prov
}
