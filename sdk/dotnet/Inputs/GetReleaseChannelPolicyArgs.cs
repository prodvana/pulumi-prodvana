// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class GetReleaseChannelPolicyInputArgs : global::Pulumi.ResourceArgs
    {
        [Input("defaultEnv", required: true)]
        private InputMap<Inputs.GetReleaseChannelPolicyDefaultEnvInputArgs>? _defaultEnv;

        /// <summary>
        /// default environment variables for services in this Release Channel
        /// </summary>
        public InputMap<Inputs.GetReleaseChannelPolicyDefaultEnvInputArgs> DefaultEnv
        {
            get => _defaultEnv ?? (_defaultEnv = new InputMap<Inputs.GetReleaseChannelPolicyDefaultEnvInputArgs>());
            set => _defaultEnv = value;
        }

        public GetReleaseChannelPolicyInputArgs()
        {
        }
        public static new GetReleaseChannelPolicyInputArgs Empty => new GetReleaseChannelPolicyInputArgs();
    }
}
