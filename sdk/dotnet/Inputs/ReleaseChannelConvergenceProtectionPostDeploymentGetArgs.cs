// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class ReleaseChannelConvergenceProtectionPostDeploymentGetArgs : global::Pulumi.ResourceArgs
    {
        [Input("checkDuration")]
        public Input<string>? CheckDuration { get; set; }

        [Input("delayCheckDuration")]
        public Input<string>? DelayCheckDuration { get; set; }

        [Input("enabled")]
        public Input<bool>? Enabled { get; set; }

        public ReleaseChannelConvergenceProtectionPostDeploymentGetArgs()
        {
        }
        public static new ReleaseChannelConvergenceProtectionPostDeploymentGetArgs Empty => new ReleaseChannelConvergenceProtectionPostDeploymentGetArgs();
    }
}