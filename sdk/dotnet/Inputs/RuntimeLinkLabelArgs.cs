// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana.Inputs
{

    public sealed class RuntimeLinkLabelArgs : global::Pulumi.ResourceArgs
    {
        /// <summary>
        /// Label name
        /// </summary>
        [Input("label", required: true)]
        public Input<string> Label { get; set; } = null!;

        /// <summary>
        /// Label value
        /// </summary>
        [Input("value", required: true)]
        public Input<string> Value { get; set; } = null!;

        public RuntimeLinkLabelArgs()
        {
        }
        public static new RuntimeLinkLabelArgs Empty => new RuntimeLinkLabelArgs();
    }
}
