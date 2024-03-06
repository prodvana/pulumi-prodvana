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
    public sealed class ReleaseChannelServiceInstanceProtectionRef
    {
        /// <summary>
        /// name of the constant
        /// </summary>
        public readonly string Name;
        /// <summary>
        /// parameters to pass to the protection
        /// </summary>
        public readonly ImmutableArray<Outputs.ReleaseChannelServiceInstanceProtectionRefParameter> Parameters;

        [OutputConstructor]
        private ReleaseChannelServiceInstanceProtectionRef(
            string name,

            ImmutableArray<Outputs.ReleaseChannelServiceInstanceProtectionRefParameter> parameters)
        {
            Name = name;
            Parameters = parameters;
        }
    }
}
