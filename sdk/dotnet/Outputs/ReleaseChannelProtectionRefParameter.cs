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
    public sealed class ReleaseChannelProtectionRefParameter
    {
        /// <summary>
        /// parameter docker image tag value, only one of (string*value, int*value, docker*image*tag*value, secret*value) can be set
        /// </summary>
        public readonly string? DockerImageTagValue;
        /// <summary>
        /// parameter int value, only one of (string*value, int*value, docker*image*tag*value, secret*value) can be set
        /// </summary>
        public readonly int? IntValue;
        /// <summary>
        /// name of the constant
        /// </summary>
        public readonly string Name;
        /// <summary>
        /// parameter secret value, only one of (string*value, int*value, docker*image*tag*value, secret*value) can be set
        /// </summary>
        public readonly Outputs.ReleaseChannelProtectionRefParameterSecretValue? SecretValue;
        /// <summary>
        /// string value of the constant
        /// </summary>
        public readonly string? StringValue;

        [OutputConstructor]
        private ReleaseChannelProtectionRefParameter(
            string? dockerImageTagValue,

            int? intValue,

            string name,

            Outputs.ReleaseChannelProtectionRefParameterSecretValue? secretValue,

            string? stringValue)
        {
            DockerImageTagValue = dockerImageTagValue;
            IntValue = intValue;
            Name = name;
            SecretValue = secretValue;
            StringValue = stringValue;
        }
    }
}
