// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Outputs
{

    [OutputType]
    public sealed class ReleaseChannelPolicyDefaultEnvSecret
    {
        public readonly string? Key;
        /// <summary>
        /// Current application version
        /// </summary>
        public readonly string? Version;

        [OutputConstructor]
        private ReleaseChannelPolicyDefaultEnvSecret(
            string? key,

            string? version)
        {
            Key = key;
            Version = version;
        }
    }
}
