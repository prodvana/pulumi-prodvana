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
    public sealed class ReleaseChannelServiceInstanceProtectionPostDeployment
    {
        /// <summary>
        /// how long to keep checking. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
        /// </summary>
        public readonly string? CheckDuration;
        /// <summary>
        /// delay between the deployment completing and when this protection starts checking. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
        /// </summary>
        public readonly string? DelayCheckDuration;
        /// <summary>
        /// whether to enable deployment lifecycle options
        /// </summary>
        public readonly bool? Enabled;

        [OutputConstructor]
        private ReleaseChannelServiceInstanceProtectionPostDeployment(
            string? checkDuration,

            string? delayCheckDuration,

            bool? enabled)
        {
            CheckDuration = checkDuration;
            DelayCheckDuration = delayCheckDuration;
            Enabled = enabled;
        }
    }
}
