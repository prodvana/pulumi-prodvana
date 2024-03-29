// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

import * as pulumi from "@pulumi/pulumi";
import * as inputs from "./types/input";
import * as outputs from "./types/output";
import * as utilities from "./utilities";

/**
 * This resource allows you to manage a Prodvana Kubernetes [Runtime](https://docs.prodvana.io/docs/prodvana-concepts#runtime). You are responsible for managing the agent lifetime. Also see `prodvana.ManagedK8sRuntime`.
 *
 * ## Example Usage
 *
 * ```typescript
 * import * as pulumi from "@pulumi/pulumi";
 * import * as prodvana from "@prodvana/pulumi-prodvana";
 *
 * const example = new prodvana.K8sRuntime("example", {labels: [
 *     {
 *         label: "env",
 *         value: "staging",
 *     },
 *     {
 *         label: "region",
 *         value: "us-central1",
 *     },
 * ]});
 * ```
 *
 * ## Import
 *
 * ```sh
 *  $ pulumi import prodvana:index/k8sRuntime:K8sRuntime example <runtime name>
 * ```
 */
export class K8sRuntime extends pulumi.CustomResource {
    /**
     * Get an existing K8sRuntime resource's state with the given name, ID, and optional extra
     * properties used to qualify the lookup.
     *
     * @param name The _unique_ name of the resulting resource.
     * @param id The _unique_ provider ID of the resource to lookup.
     * @param state Any extra arguments used during the lookup.
     * @param opts Optional settings to control the behavior of the CustomResource.
     */
    public static get(name: string, id: pulumi.Input<pulumi.ID>, state?: K8sRuntimeState, opts?: pulumi.CustomResourceOptions): K8sRuntime {
        return new K8sRuntime(name, <any>state, { ...opts, id: id });
    }

    /** @internal */
    public static readonly __pulumiType = 'prodvana:index/k8sRuntime:K8sRuntime';

    /**
     * Returns true if the given object is an instance of K8sRuntime.  This is designed to work even
     * when multiple copies of the Pulumi SDK have been loaded into the same process.
     */
    public static isInstance(obj: any): obj is K8sRuntime {
        if (obj === undefined || obj === null) {
            return false;
        }
        return obj['__pulumiType'] === K8sRuntime.__pulumiType;
    }

    /**
     * API Token used for linking the Kubernetes Prodvana agent
     */
    public /*out*/ readonly agentApiToken!: pulumi.Output<string>;
    /**
     * Arguments to pass to the Kubernetes Prodvana agent container.
     */
    public /*out*/ readonly agentArgs!: pulumi.Output<string[]>;
    /**
     * URL of the Kubernetes Prodvana agent container image.
     */
    public /*out*/ readonly agentImage!: pulumi.Output<string>;
    /**
     * URL of the Kubernetes Prodvana agent server
     */
    public /*out*/ readonly agentUrl!: pulumi.Output<string>;
    /**
     * List of labels to apply to the runtime
     */
    public readonly labels!: pulumi.Output<outputs.K8sRuntimeLabel[]>;
    /**
     * Runtime name
     */
    public readonly name!: pulumi.Output<string>;

    /**
     * Create a K8sRuntime resource with the given unique name, arguments, and options.
     *
     * @param name The _unique_ name of the resource.
     * @param args The arguments to use to populate this resource's properties.
     * @param opts A bag of options that control this resource's behavior.
     */
    constructor(name: string, args?: K8sRuntimeArgs, opts?: pulumi.CustomResourceOptions)
    constructor(name: string, argsOrState?: K8sRuntimeArgs | K8sRuntimeState, opts?: pulumi.CustomResourceOptions) {
        let resourceInputs: pulumi.Inputs = {};
        opts = opts || {};
        if (opts.id) {
            const state = argsOrState as K8sRuntimeState | undefined;
            resourceInputs["agentApiToken"] = state ? state.agentApiToken : undefined;
            resourceInputs["agentArgs"] = state ? state.agentArgs : undefined;
            resourceInputs["agentImage"] = state ? state.agentImage : undefined;
            resourceInputs["agentUrl"] = state ? state.agentUrl : undefined;
            resourceInputs["labels"] = state ? state.labels : undefined;
            resourceInputs["name"] = state ? state.name : undefined;
        } else {
            const args = argsOrState as K8sRuntimeArgs | undefined;
            resourceInputs["labels"] = args ? args.labels : undefined;
            resourceInputs["name"] = args ? args.name : undefined;
            resourceInputs["agentApiToken"] = undefined /*out*/;
            resourceInputs["agentArgs"] = undefined /*out*/;
            resourceInputs["agentImage"] = undefined /*out*/;
            resourceInputs["agentUrl"] = undefined /*out*/;
        }
        opts = pulumi.mergeOptions(utilities.resourceOptsDefaults(), opts);
        const secretOpts = { additionalSecretOutputs: ["agentApiToken", "agentArgs"] };
        opts = pulumi.mergeOptions(opts, secretOpts);
        super(K8sRuntime.__pulumiType, name, resourceInputs, opts);
    }
}

/**
 * Input properties used for looking up and filtering K8sRuntime resources.
 */
export interface K8sRuntimeState {
    /**
     * API Token used for linking the Kubernetes Prodvana agent
     */
    agentApiToken?: pulumi.Input<string>;
    /**
     * Arguments to pass to the Kubernetes Prodvana agent container.
     */
    agentArgs?: pulumi.Input<pulumi.Input<string>[]>;
    /**
     * URL of the Kubernetes Prodvana agent container image.
     */
    agentImage?: pulumi.Input<string>;
    /**
     * URL of the Kubernetes Prodvana agent server
     */
    agentUrl?: pulumi.Input<string>;
    /**
     * List of labels to apply to the runtime
     */
    labels?: pulumi.Input<pulumi.Input<inputs.K8sRuntimeLabel>[]>;
    /**
     * Runtime name
     */
    name?: pulumi.Input<string>;
}

/**
 * The set of arguments for constructing a K8sRuntime resource.
 */
export interface K8sRuntimeArgs {
    /**
     * List of labels to apply to the runtime
     */
    labels?: pulumi.Input<pulumi.Input<inputs.K8sRuntimeLabel>[]>;
    /**
     * Runtime name
     */
    name?: pulumi.Input<string>;
}
