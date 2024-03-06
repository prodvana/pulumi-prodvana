// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class GetReleaseChannelProtectionPostDeploymentArgs : global::Pulumi.InvokeArgs
    {
        /// <summary>
        /// how long to keep checking. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
        /// </summary>
        [Input("checkDuration")]
        public string? CheckDuration { get; set; }

        /// <summary>
        /// delay between the deployment completing and when this protection starts checking. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
        /// </summary>
        [Input("delayCheckDuration")]
        public string? DelayCheckDuration { get; set; }

        /// <summary>
        /// whether to enable deployment lifecycle options
        /// </summary>
        [Input("enabled", required: true)]
        public bool Enabled { get; set; }

        public GetReleaseChannelProtectionPostDeploymentArgs()
        {
        }
        public static new GetReleaseChannelProtectionPostDeploymentArgs Empty => new GetReleaseChannelProtectionPostDeploymentArgs();
    }
}
