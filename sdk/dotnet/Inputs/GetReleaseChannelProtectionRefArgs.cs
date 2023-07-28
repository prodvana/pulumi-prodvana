// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class GetReleaseChannelProtectionRefInputArgs : global::Pulumi.ResourceArgs
    {
        /// <summary>
        /// Release Channel name
        /// </summary>
        [Input("name", required: true)]
        public Input<string> Name { get; set; } = null!;

        [Input("parameters")]
        private InputList<Inputs.GetReleaseChannelProtectionRefParameterInputArgs>? _parameters;
        public InputList<Inputs.GetReleaseChannelProtectionRefParameterInputArgs> Parameters
        {
            get => _parameters ?? (_parameters = new InputList<Inputs.GetReleaseChannelProtectionRefParameterInputArgs>());
            set => _parameters = value;
        }

        public GetReleaseChannelProtectionRefInputArgs()
        {
        }
        public static new GetReleaseChannelProtectionRefInputArgs Empty => new GetReleaseChannelProtectionRefInputArgs();
    }
}
