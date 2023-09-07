// Code generated by the Pulumi Terraform Bridge (tfgen) Tool DO NOT EDIT.
// *** WARNING: Do not edit by hand unless you're certain you know what you are doing! ***

package prodvana

import (
	"context"
	"reflect"

	"github.com/prodvana/pulumi-prodvana/sdk/go/prodvana/internal"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

// (Alpha! This feature is still in progress.)
// A `runtimeLink` resource represents a successfully linked runtime.
// This is most useful for Kubernetes runtimes -- the agent must be installed and registered with the Prodvana service before the runtime can be used.
// Pair this with an explicit `dependsOn` block ensures that the runtime is ready before attempting to use it. See the example below.
type RuntimeLink struct {
	pulumi.CustomResourceState

	// List of labels to apply to the runtime
	Labels RuntimeLinkLabelArrayOutput `pulumi:"labels"`
	// Name of the runtime to wait for linking.
	Name pulumi.StringOutput `pulumi:"name"`
	// How long to wait for the runtime linking to complete. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
	Timeout pulumi.StringOutput `pulumi:"timeout"`
}

// NewRuntimeLink registers a new resource with the given unique name, arguments, and options.
func NewRuntimeLink(ctx *pulumi.Context,
	name string, args *RuntimeLinkArgs, opts ...pulumi.ResourceOption) (*RuntimeLink, error) {
	if args == nil {
		args = &RuntimeLinkArgs{}
	}

	opts = internal.PkgResourceDefaultOpts(opts)
	var resource RuntimeLink
	err := ctx.RegisterResource("prodvana:index/runtimeLink:RuntimeLink", name, args, &resource, opts...)
	if err != nil {
		return nil, err
	}
	return &resource, nil
}

// GetRuntimeLink gets an existing RuntimeLink resource's state with the given name, ID, and optional
// state properties that are used to uniquely qualify the lookup (nil if not required).
func GetRuntimeLink(ctx *pulumi.Context,
	name string, id pulumi.IDInput, state *RuntimeLinkState, opts ...pulumi.ResourceOption) (*RuntimeLink, error) {
	var resource RuntimeLink
	err := ctx.ReadResource("prodvana:index/runtimeLink:RuntimeLink", name, id, state, &resource, opts...)
	if err != nil {
		return nil, err
	}
	return &resource, nil
}

// Input properties used for looking up and filtering RuntimeLink resources.
type runtimeLinkState struct {
	// List of labels to apply to the runtime
	Labels []RuntimeLinkLabel `pulumi:"labels"`
	// Name of the runtime to wait for linking.
	Name *string `pulumi:"name"`
	// How long to wait for the runtime linking to complete. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
	Timeout *string `pulumi:"timeout"`
}

type RuntimeLinkState struct {
	// List of labels to apply to the runtime
	Labels RuntimeLinkLabelArrayInput
	// Name of the runtime to wait for linking.
	Name pulumi.StringPtrInput
	// How long to wait for the runtime linking to complete. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
	Timeout pulumi.StringPtrInput
}

func (RuntimeLinkState) ElementType() reflect.Type {
	return reflect.TypeOf((*runtimeLinkState)(nil)).Elem()
}

type runtimeLinkArgs struct {
	// List of labels to apply to the runtime
	Labels []RuntimeLinkLabel `pulumi:"labels"`
	// Name of the runtime to wait for linking.
	Name *string `pulumi:"name"`
	// How long to wait for the runtime linking to complete. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
	Timeout *string `pulumi:"timeout"`
}

// The set of arguments for constructing a RuntimeLink resource.
type RuntimeLinkArgs struct {
	// List of labels to apply to the runtime
	Labels RuntimeLinkLabelArrayInput
	// Name of the runtime to wait for linking.
	Name pulumi.StringPtrInput
	// How long to wait for the runtime linking to complete. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
	Timeout pulumi.StringPtrInput
}

func (RuntimeLinkArgs) ElementType() reflect.Type {
	return reflect.TypeOf((*runtimeLinkArgs)(nil)).Elem()
}

type RuntimeLinkInput interface {
	pulumi.Input

	ToRuntimeLinkOutput() RuntimeLinkOutput
	ToRuntimeLinkOutputWithContext(ctx context.Context) RuntimeLinkOutput
}

func (*RuntimeLink) ElementType() reflect.Type {
	return reflect.TypeOf((**RuntimeLink)(nil)).Elem()
}

func (i *RuntimeLink) ToRuntimeLinkOutput() RuntimeLinkOutput {
	return i.ToRuntimeLinkOutputWithContext(context.Background())
}

func (i *RuntimeLink) ToRuntimeLinkOutputWithContext(ctx context.Context) RuntimeLinkOutput {
	return pulumi.ToOutputWithContext(ctx, i).(RuntimeLinkOutput)
}

// RuntimeLinkArrayInput is an input type that accepts RuntimeLinkArray and RuntimeLinkArrayOutput values.
// You can construct a concrete instance of `RuntimeLinkArrayInput` via:
//
//	RuntimeLinkArray{ RuntimeLinkArgs{...} }
type RuntimeLinkArrayInput interface {
	pulumi.Input

	ToRuntimeLinkArrayOutput() RuntimeLinkArrayOutput
	ToRuntimeLinkArrayOutputWithContext(context.Context) RuntimeLinkArrayOutput
}

type RuntimeLinkArray []RuntimeLinkInput

func (RuntimeLinkArray) ElementType() reflect.Type {
	return reflect.TypeOf((*[]*RuntimeLink)(nil)).Elem()
}

func (i RuntimeLinkArray) ToRuntimeLinkArrayOutput() RuntimeLinkArrayOutput {
	return i.ToRuntimeLinkArrayOutputWithContext(context.Background())
}

func (i RuntimeLinkArray) ToRuntimeLinkArrayOutputWithContext(ctx context.Context) RuntimeLinkArrayOutput {
	return pulumi.ToOutputWithContext(ctx, i).(RuntimeLinkArrayOutput)
}

// RuntimeLinkMapInput is an input type that accepts RuntimeLinkMap and RuntimeLinkMapOutput values.
// You can construct a concrete instance of `RuntimeLinkMapInput` via:
//
//	RuntimeLinkMap{ "key": RuntimeLinkArgs{...} }
type RuntimeLinkMapInput interface {
	pulumi.Input

	ToRuntimeLinkMapOutput() RuntimeLinkMapOutput
	ToRuntimeLinkMapOutputWithContext(context.Context) RuntimeLinkMapOutput
}

type RuntimeLinkMap map[string]RuntimeLinkInput

func (RuntimeLinkMap) ElementType() reflect.Type {
	return reflect.TypeOf((*map[string]*RuntimeLink)(nil)).Elem()
}

func (i RuntimeLinkMap) ToRuntimeLinkMapOutput() RuntimeLinkMapOutput {
	return i.ToRuntimeLinkMapOutputWithContext(context.Background())
}

func (i RuntimeLinkMap) ToRuntimeLinkMapOutputWithContext(ctx context.Context) RuntimeLinkMapOutput {
	return pulumi.ToOutputWithContext(ctx, i).(RuntimeLinkMapOutput)
}

type RuntimeLinkOutput struct{ *pulumi.OutputState }

func (RuntimeLinkOutput) ElementType() reflect.Type {
	return reflect.TypeOf((**RuntimeLink)(nil)).Elem()
}

func (o RuntimeLinkOutput) ToRuntimeLinkOutput() RuntimeLinkOutput {
	return o
}

func (o RuntimeLinkOutput) ToRuntimeLinkOutputWithContext(ctx context.Context) RuntimeLinkOutput {
	return o
}

// List of labels to apply to the runtime
func (o RuntimeLinkOutput) Labels() RuntimeLinkLabelArrayOutput {
	return o.ApplyT(func(v *RuntimeLink) RuntimeLinkLabelArrayOutput { return v.Labels }).(RuntimeLinkLabelArrayOutput)
}

// Name of the runtime to wait for linking.
func (o RuntimeLinkOutput) Name() pulumi.StringOutput {
	return o.ApplyT(func(v *RuntimeLink) pulumi.StringOutput { return v.Name }).(pulumi.StringOutput)
}

// How long to wait for the runtime linking to complete. A valid Go duration string, e.g. `10m` or `1h`. Defaults to `10m`
func (o RuntimeLinkOutput) Timeout() pulumi.StringOutput {
	return o.ApplyT(func(v *RuntimeLink) pulumi.StringOutput { return v.Timeout }).(pulumi.StringOutput)
}

type RuntimeLinkArrayOutput struct{ *pulumi.OutputState }

func (RuntimeLinkArrayOutput) ElementType() reflect.Type {
	return reflect.TypeOf((*[]*RuntimeLink)(nil)).Elem()
}

func (o RuntimeLinkArrayOutput) ToRuntimeLinkArrayOutput() RuntimeLinkArrayOutput {
	return o
}

func (o RuntimeLinkArrayOutput) ToRuntimeLinkArrayOutputWithContext(ctx context.Context) RuntimeLinkArrayOutput {
	return o
}

func (o RuntimeLinkArrayOutput) Index(i pulumi.IntInput) RuntimeLinkOutput {
	return pulumi.All(o, i).ApplyT(func(vs []interface{}) *RuntimeLink {
		return vs[0].([]*RuntimeLink)[vs[1].(int)]
	}).(RuntimeLinkOutput)
}

type RuntimeLinkMapOutput struct{ *pulumi.OutputState }

func (RuntimeLinkMapOutput) ElementType() reflect.Type {
	return reflect.TypeOf((*map[string]*RuntimeLink)(nil)).Elem()
}

func (o RuntimeLinkMapOutput) ToRuntimeLinkMapOutput() RuntimeLinkMapOutput {
	return o
}

func (o RuntimeLinkMapOutput) ToRuntimeLinkMapOutputWithContext(ctx context.Context) RuntimeLinkMapOutput {
	return o
}

func (o RuntimeLinkMapOutput) MapIndex(k pulumi.StringInput) RuntimeLinkOutput {
	return pulumi.All(o, k).ApplyT(func(vs []interface{}) *RuntimeLink {
		return vs[0].(map[string]*RuntimeLink)[vs[1].(string)]
	}).(RuntimeLinkOutput)
}

func init() {
	pulumi.RegisterInputType(reflect.TypeOf((*RuntimeLinkInput)(nil)).Elem(), &RuntimeLink{})
	pulumi.RegisterInputType(reflect.TypeOf((*RuntimeLinkArrayInput)(nil)).Elem(), RuntimeLinkArray{})
	pulumi.RegisterInputType(reflect.TypeOf((*RuntimeLinkMapInput)(nil)).Elem(), RuntimeLinkMap{})
	pulumi.RegisterOutputType(RuntimeLinkOutput{})
	pulumi.RegisterOutputType(RuntimeLinkArrayOutput{})
	pulumi.RegisterOutputType(RuntimeLinkMapOutput{})
}
