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
    public sealed class ReleaseChannelProtection
    {
        /// <summary>
        /// deployment lifecycle options
        /// </summary>
        public readonly Outputs.ReleaseChannelProtectionDeployment? Deployment;
        /// <summary>
        /// name of the protection
        /// </summary>
        public readonly string? Name;
        /// <summary>
        /// post-approval lifecycle options
        /// </summary>
        public readonly Outputs.ReleaseChannelProtectionPostApproval? PostApproval;
        /// <summary>
        /// post-deployment lifecycle options
        /// </summary>
        public readonly Outputs.ReleaseChannelProtectionPostDeployment? PostDeployment;
        /// <summary>
        /// pre-approval lifecycle options
        /// </summary>
        public readonly Outputs.ReleaseChannelProtectionPreApproval? PreApproval;
        /// <summary>
        /// reference to a protection stored in Prodvana
        /// </summary>
        public readonly Outputs.ReleaseChannelProtectionRef Ref;

        [OutputConstructor]
        private ReleaseChannelProtection(
            Outputs.ReleaseChannelProtectionDeployment? deployment,

            string? name,

            Outputs.ReleaseChannelProtectionPostApproval? postApproval,

            Outputs.ReleaseChannelProtectionPostDeployment? postDeployment,

            Outputs.ReleaseChannelProtectionPreApproval? preApproval,

            Outputs.ReleaseChannelProtectionRef @ref)
        {
            Deployment = deployment;
            Name = name;
            PostApproval = postApproval;
            PostDeployment = postDeployment;
            PreApproval = preApproval;
            Ref = @ref;
        }
    }
}