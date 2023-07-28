// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class GetReleaseChannelProtectionRefArgs : global::Pulumi.InvokeArgs
    {
        /// <summary>
        /// Release Channel name
        /// </summary>
        [Input("name", required: true)]
        public string Name { get; set; } = null!;

        [Input("parameters")]
        private List<Inputs.GetReleaseChannelProtectionRefParameterArgs>? _parameters;
        public List<Inputs.GetReleaseChannelProtectionRefParameterArgs> Parameters
        {
            get => _parameters ?? (_parameters = new List<Inputs.GetReleaseChannelProtectionRefParameterArgs>());
            set => _parameters = value;
        }

        public GetReleaseChannelProtectionRefArgs()
        {
        }
        public static new GetReleaseChannelProtectionRefArgs Empty => new GetReleaseChannelProtectionRefArgs();
    }
}
