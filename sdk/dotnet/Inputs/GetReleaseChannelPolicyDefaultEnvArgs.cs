// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class GetReleaseChannelPolicyDefaultEnvInputArgs : global::Pulumi.ResourceArgs
    {
        /// <summary>
        /// Reference to a secret value stored in Kubernetes.
        /// </summary>
        [Input("kubernetesSecret")]
        public Input<Inputs.GetReleaseChannelPolicyDefaultEnvKubernetesSecretInputArgs>? KubernetesSecret { get; set; }

        /// <summary>
        /// Reference to a secret value stored in Prodvana.
        /// </summary>
        [Input("secret")]
        public Input<Inputs.GetReleaseChannelPolicyDefaultEnvSecretInputArgs>? Secret { get; set; }

        /// <summary>
        /// Non-sensitive environment variable value
        /// </summary>
        [Input("value")]
        public Input<string>? Value { get; set; }

        public GetReleaseChannelPolicyDefaultEnvInputArgs()
        {
        }
        public static new GetReleaseChannelPolicyDefaultEnvInputArgs Empty => new GetReleaseChannelPolicyDefaultEnvInputArgs();
    }
}
