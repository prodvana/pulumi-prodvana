// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class ReleaseChannelServiceInstanceProtectionArgs : global::Pulumi.ResourceArgs
    {
        /// <summary>
        /// deployment lifecycle options
        /// </summary>
        [Input("deployment")]
        public Input<Inputs.ReleaseChannelServiceInstanceProtectionDeploymentArgs>? Deployment { get; set; }

        /// <summary>
        /// name of the protection
        /// </summary>
        [Input("name")]
        public Input<string>? Name { get; set; }

        /// <summary>
        /// post-approval lifecycle options
        /// </summary>
        [Input("postApproval")]
        public Input<Inputs.ReleaseChannelServiceInstanceProtectionPostApprovalArgs>? PostApproval { get; set; }

        /// <summary>
        /// post-deployment lifecycle options
        /// </summary>
        [Input("postDeployment")]
        public Input<Inputs.ReleaseChannelServiceInstanceProtectionPostDeploymentArgs>? PostDeployment { get; set; }

        /// <summary>
        /// pre-approval lifecycle options
        /// </summary>
        [Input("preApproval")]
        public Input<Inputs.ReleaseChannelServiceInstanceProtectionPreApprovalArgs>? PreApproval { get; set; }

        /// <summary>
        /// reference to a protection stored in Prodvana
        /// </summary>
        [Input("ref", required: true)]
        public Input<Inputs.ReleaseChannelServiceInstanceProtectionRefArgs> Ref { get; set; } = null!;

        public ReleaseChannelServiceInstanceProtectionArgs()
        {
        }
        public static new ReleaseChannelServiceInstanceProtectionArgs Empty => new ReleaseChannelServiceInstanceProtectionArgs();
    }
}