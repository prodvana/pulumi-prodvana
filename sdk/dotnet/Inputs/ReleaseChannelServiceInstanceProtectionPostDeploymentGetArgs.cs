// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class ReleaseChannelServiceInstanceProtectionPostDeploymentGetArgs : global::Pulumi.ResourceArgs
    {
        /// <summary>
        /// how long to keep checking. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
        /// </summary>
        [Input("checkDuration")]
        public Input<string>? CheckDuration { get; set; }

        /// <summary>
        /// delay between the deployment completing and when this protection starts checking. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
        /// </summary>
        [Input("delayCheckDuration")]
        public Input<string>? DelayCheckDuration { get; set; }

        /// <summary>
        /// whether to enable deployment lifecycle options
        /// </summary>
        [Input("enabled")]
        public Input<bool>? Enabled { get; set; }

        public ReleaseChannelServiceInstanceProtectionPostDeploymentGetArgs()
        {
        }
        public static new ReleaseChannelServiceInstanceProtectionPostDeploymentGetArgs Empty => new ReleaseChannelServiceInstanceProtectionPostDeploymentGetArgs();
    }
}
