// *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

import * as pulumi from "@pulumi/pulumi";
import * as inputs from "./types/input";
import * as outputs from "./types/output";
import * as utilities from "./utilities";

/**
 * This resource allows you to manage a Prodvana [Release Channel](https://docs.prodvana.io/docs/prodvana-concepts#release-channel).
 *
 * ## Import
 *
 * ```sh
 *  $ pulumi import prodvana:index/releaseChannel:ReleaseChannel example <application name>/<release channel name>
 * ```
 */
export class ReleaseChannel extends pulumi.CustomResource {
    /**
     * Get an existing ReleaseChannel resource's state with the given name, ID, and optional extra
     * properties used to qualify the lookup.
     *
     * @param name The _unique_ name of the resulting resource.
     * @param id The _unique_ provider ID of the resource to lookup.
     * @param state Any extra arguments used during the lookup.
     * @param opts Optional settings to control the behavior of the CustomResource.
     */
    public static get(name: string, id: pulumi.Input<pulumi.ID>, state?: ReleaseChannelState, opts?: pulumi.CustomResourceOptions): ReleaseChannel {
        return new ReleaseChannel(name, <any>state, { ...opts, id: id });
    }

    /** @internal */
    public static readonly __pulumiType = 'prodvana:index/releaseChannel:ReleaseChannel';

    /**
     * Returns true if the given object is an instance of ReleaseChannel.  This is designed to work even
     * when multiple copies of the Pulumi SDK have been loaded into the same process.
     */
    public static isInstance(obj: any): obj is ReleaseChannel {
        if (obj === undefined || obj === null) {
            return false;
        }
        return obj['__pulumiType'] === ReleaseChannel.__pulumiType;
    }

    /**
     * Name of the Application this Release Channel belongs to
     */
    public readonly application!: pulumi.Output<string>;
    /**
     * Constant values for this release channel
     */
    public readonly constants!: pulumi.Output<outputs.ReleaseChannelConstant[] | undefined>;
    /**
     * Feature Coming Soon
     */
    public readonly convergenceProtections!: pulumi.Output<outputs.ReleaseChannelConvergenceProtection[] | undefined>;
    /**
     * Preconditions requiring manual approval before this release channel can be deployed
     */
    public readonly manualApprovalPreconditions!: pulumi.Output<outputs.ReleaseChannelManualApprovalPrecondition[] | undefined>;
    /**
     * Release Channel name
     */
    public readonly name!: pulumi.Output<string>;
    /**
     * Release Channel policy applied to all services
     */
    public readonly policy!: pulumi.Output<outputs.ReleaseChannelPolicy | undefined>;
    /**
     * Protections applied this release channel
     */
    public readonly protections!: pulumi.Output<outputs.ReleaseChannelProtection[] | undefined>;
    /**
     * Preconditions requiring other release channels to be stable before this release channel can be deployed
     */
    public readonly releaseChannelStablePreconditions!: pulumi.Output<outputs.ReleaseChannelReleaseChannelStablePrecondition[] | undefined>;
    /**
     * Release Channel policy applied to all services
     */
    public readonly runtimes!: pulumi.Output<outputs.ReleaseChannelRuntime[]>;
    /**
     * Protections applied to service instances in this release channel
     */
    public readonly serviceInstanceProtections!: pulumi.Output<outputs.ReleaseChannelServiceInstanceProtection[] | undefined>;
    /**
     * Current application version
     */
    public /*out*/ readonly version!: pulumi.Output<string>;

    /**
     * Create a ReleaseChannel resource with the given unique name, arguments, and options.
     *
     * @param name The _unique_ name of the resource.
     * @param args The arguments to use to populate this resource's properties.
     * @param opts A bag of options that control this resource's behavior.
     */
    constructor(name: string, args: ReleaseChannelArgs, opts?: pulumi.CustomResourceOptions)
    constructor(name: string, argsOrState?: ReleaseChannelArgs | ReleaseChannelState, opts?: pulumi.CustomResourceOptions) {
        let resourceInputs: pulumi.Inputs = {};
        opts = opts || {};
        if (opts.id) {
            const state = argsOrState as ReleaseChannelState | undefined;
            resourceInputs["application"] = state ? state.application : undefined;
            resourceInputs["constants"] = state ? state.constants : undefined;
            resourceInputs["convergenceProtections"] = state ? state.convergenceProtections : undefined;
            resourceInputs["manualApprovalPreconditions"] = state ? state.manualApprovalPreconditions : undefined;
            resourceInputs["name"] = state ? state.name : undefined;
            resourceInputs["policy"] = state ? state.policy : undefined;
            resourceInputs["protections"] = state ? state.protections : undefined;
            resourceInputs["releaseChannelStablePreconditions"] = state ? state.releaseChannelStablePreconditions : undefined;
            resourceInputs["runtimes"] = state ? state.runtimes : undefined;
            resourceInputs["serviceInstanceProtections"] = state ? state.serviceInstanceProtections : undefined;
            resourceInputs["version"] = state ? state.version : undefined;
        } else {
            const args = argsOrState as ReleaseChannelArgs | undefined;
            if ((!args || args.application === undefined) && !opts.urn) {
                throw new Error("Missing required property 'application'");
            }
            if ((!args || args.runtimes === undefined) && !opts.urn) {
                throw new Error("Missing required property 'runtimes'");
            }
            resourceInputs["application"] = args ? args.application : undefined;
            resourceInputs["constants"] = args ? args.constants : undefined;
            resourceInputs["convergenceProtections"] = args ? args.convergenceProtections : undefined;
            resourceInputs["manualApprovalPreconditions"] = args ? args.manualApprovalPreconditions : undefined;
            resourceInputs["name"] = args ? args.name : undefined;
            resourceInputs["policy"] = args ? args.policy : undefined;
            resourceInputs["protections"] = args ? args.protections : undefined;
            resourceInputs["releaseChannelStablePreconditions"] = args ? args.releaseChannelStablePreconditions : undefined;
            resourceInputs["runtimes"] = args ? args.runtimes : undefined;
            resourceInputs["serviceInstanceProtections"] = args ? args.serviceInstanceProtections : undefined;
            resourceInputs["version"] = undefined /*out*/;
        }
        opts = pulumi.mergeOptions(utilities.resourceOptsDefaults(), opts);
        super(ReleaseChannel.__pulumiType, name, resourceInputs, opts);
    }
}

/**
 * Input properties used for looking up and filtering ReleaseChannel resources.
 */
export interface ReleaseChannelState {
    /**
     * Name of the Application this Release Channel belongs to
     */
    application?: pulumi.Input<string>;
    /**
     * Constant values for this release channel
     */
    constants?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelConstant>[]>;
    /**
     * Feature Coming Soon
     */
    convergenceProtections?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelConvergenceProtection>[]>;
    /**
     * Preconditions requiring manual approval before this release channel can be deployed
     */
    manualApprovalPreconditions?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelManualApprovalPrecondition>[]>;
    /**
     * Release Channel name
     */
    name?: pulumi.Input<string>;
    /**
     * Release Channel policy applied to all services
     */
    policy?: pulumi.Input<inputs.ReleaseChannelPolicy>;
    /**
     * Protections applied this release channel
     */
    protections?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelProtection>[]>;
    /**
     * Preconditions requiring other release channels to be stable before this release channel can be deployed
     */
    releaseChannelStablePreconditions?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelReleaseChannelStablePrecondition>[]>;
    /**
     * Release Channel policy applied to all services
     */
    runtimes?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelRuntime>[]>;
    /**
     * Protections applied to service instances in this release channel
     */
    serviceInstanceProtections?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelServiceInstanceProtection>[]>;
    /**
     * Current application version
     */
    version?: pulumi.Input<string>;
}

/**
 * The set of arguments for constructing a ReleaseChannel resource.
 */
export interface ReleaseChannelArgs {
    /**
     * Name of the Application this Release Channel belongs to
     */
    application: pulumi.Input<string>;
    /**
     * Constant values for this release channel
     */
    constants?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelConstant>[]>;
    /**
     * Feature Coming Soon
     */
    convergenceProtections?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelConvergenceProtection>[]>;
    /**
     * Preconditions requiring manual approval before this release channel can be deployed
     */
    manualApprovalPreconditions?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelManualApprovalPrecondition>[]>;
    /**
     * Release Channel name
     */
    name?: pulumi.Input<string>;
    /**
     * Release Channel policy applied to all services
     */
    policy?: pulumi.Input<inputs.ReleaseChannelPolicy>;
    /**
     * Protections applied this release channel
     */
    protections?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelProtection>[]>;
    /**
     * Preconditions requiring other release channels to be stable before this release channel can be deployed
     */
    releaseChannelStablePreconditions?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelReleaseChannelStablePrecondition>[]>;
    /**
     * Release Channel policy applied to all services
     */
    runtimes: pulumi.Input<pulumi.Input<inputs.ReleaseChannelRuntime>[]>;
    /**
     * Protections applied to service instances in this release channel
     */
    serviceInstanceProtections?: pulumi.Input<pulumi.Input<inputs.ReleaseChannelServiceInstanceProtection>[]>;
}
