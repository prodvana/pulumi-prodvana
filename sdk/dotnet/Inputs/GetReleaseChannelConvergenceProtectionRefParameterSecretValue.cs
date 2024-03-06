// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class GetReleaseChannelConvergenceProtectionRefParameterSecretValueArgs : global::Pulumi.InvokeArgs
    {
        /// <summary>
        /// Name of the secret.
        /// </summary>
        [Input("key", required: true)]
        public string Key { get; set; } = null!;

        /// <summary>
        /// Version of the secret
        /// </summary>
        [Input("version", required: true)]
        public string Version { get; set; } = null!;

        public GetReleaseChannelConvergenceProtectionRefParameterSecretValueArgs()
        {
        }
        public static new GetReleaseChannelConvergenceProtectionRefParameterSecretValueArgs Empty => new GetReleaseChannelConvergenceProtectionRefParameterSecretValueArgs();
    }
}
