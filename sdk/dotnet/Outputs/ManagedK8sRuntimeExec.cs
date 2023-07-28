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
    public sealed class ManagedK8sRuntimeExec
    {
        /// <summary>
        /// API version of the exec credential plugin
        /// </summary>
        public readonly string ApiVersion;
        /// <summary>
        /// Arguments to pass when executing the command
        /// </summary>
        public readonly ImmutableArray<string> Args;
        /// <summary>
        /// Command to execute
        /// </summary>
        public readonly string Command;
        /// <summary>
        /// Environment variables to set when executing the command
        /// </summary>
        public readonly ImmutableDictionary<string, string>? Env;

        [OutputConstructor]
        private ManagedK8sRuntimeExec(
            string apiVersion,

            ImmutableArray<string> args,

            string command,

            ImmutableDictionary<string, string>? env)
        {
            ApiVersion = apiVersion;
            Args = args;
            Command = command;
            Env = env;
        }
    }
}
