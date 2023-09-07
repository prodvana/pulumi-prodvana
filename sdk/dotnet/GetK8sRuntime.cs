// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Prodvana
{
    public static class GetK8sRuntime
    {
        /// <summary>
        /// Prodvana Kubernetes Runtime
        /// </summary>
        public static Task<GetK8sRuntimeResult> InvokeAsync(GetK8sRuntimeArgs args, InvokeOptions? options = null)
            => global::Pulumi.Deployment.Instance.InvokeAsync<GetK8sRuntimeResult>("prodvana:index/getK8sRuntime:getK8sRuntime", args ?? new GetK8sRuntimeArgs(), options.WithDefaults());

        /// <summary>
        /// Prodvana Kubernetes Runtime
        /// </summary>
        public static Output<GetK8sRuntimeResult> Invoke(GetK8sRuntimeInvokeArgs args, InvokeOptions? options = null)
            => global::Pulumi.Deployment.Instance.Invoke<GetK8sRuntimeResult>("prodvana:index/getK8sRuntime:getK8sRuntime", args ?? new GetK8sRuntimeInvokeArgs(), options.WithDefaults());
    }


    public sealed class GetK8sRuntimeArgs : global::Pulumi.InvokeArgs
    {
        [Input("labels")]
        private List<Inputs.GetK8sRuntimeLabelArgs>? _labels;

        /// <summary>
        /// List of labels to apply to the runtime
        /// </summary>
        public List<Inputs.GetK8sRuntimeLabelArgs> Labels
        {
            get => _labels ?? (_labels = new List<Inputs.GetK8sRuntimeLabelArgs>());
            set => _labels = value;
        }

        /// <summary>
        /// Runtime name
        /// </summary>
        [Input("name", required: true)]
        public string Name { get; set; } = null!;

        public GetK8sRuntimeArgs()
        {
        }
        public static new GetK8sRuntimeArgs Empty => new GetK8sRuntimeArgs();
    }

    public sealed class GetK8sRuntimeInvokeArgs : global::Pulumi.InvokeArgs
    {
        [Input("labels")]
        private InputList<Inputs.GetK8sRuntimeLabelInputArgs>? _labels;

        /// <summary>
        /// List of labels to apply to the runtime
        /// </summary>
        public InputList<Inputs.GetK8sRuntimeLabelInputArgs> Labels
        {
            get => _labels ?? (_labels = new InputList<Inputs.GetK8sRuntimeLabelInputArgs>());
            set => _labels = value;
        }

        /// <summary>
        /// Runtime name
        /// </summary>
        [Input("name", required: true)]
        public Input<string> Name { get; set; } = null!;

        public GetK8sRuntimeInvokeArgs()
        {
        }
        public static new GetK8sRuntimeInvokeArgs Empty => new GetK8sRuntimeInvokeArgs();
    }


    [OutputType]
    public sealed class GetK8sRuntimeResult
    {
        /// <summary>
        /// API Token used for linking the Kubernetes Prodvana agent
        /// </summary>
        public readonly string AgentApiToken;
        /// <summary>
        /// Runtime identifier
        /// </summary>
        public readonly string Id;
        /// <summary>
        /// List of labels to apply to the runtime
        /// </summary>
        public readonly ImmutableArray<Outputs.GetK8sRuntimeLabelResult> Labels;
        /// <summary>
        /// Runtime name
        /// </summary>
        public readonly string Name;

        [OutputConstructor]
        private GetK8sRuntimeResult(
            string agentApiToken,

            string id,

            ImmutableArray<Outputs.GetK8sRuntimeLabelResult> labels,

            string name)
        {
            AgentApiToken = agentApiToken;
            Id = id;
            Labels = labels;
            Name = name;
        }
    }
}
