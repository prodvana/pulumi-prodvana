// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class ReleaseChannelPolicyDefaultEnvKubernetesSecretArgs : global::Pulumi.ResourceArgs
    {
        [Input("key")]
        public Input<string>? Key { get; set; }

        [Input("secretName")]
        public Input<string>? SecretName { get; set; }

        public ReleaseChannelPolicyDefaultEnvKubernetesSecretArgs()
        {
        }
        public static new ReleaseChannelPolicyDefaultEnvKubernetesSecretArgs Empty => new ReleaseChannelPolicyDefaultEnvKubernetesSecretArgs();
    }
}
