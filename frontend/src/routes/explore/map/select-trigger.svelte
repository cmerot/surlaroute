<script lang="ts">
	import { cn } from "$lib/utils.js";
	import { Select as SelectPrimitive, type WithoutChild } from "bits-ui";

	let {
		ref = $bindable(null),
		class: className,
		children,
		...restProps
	}: WithoutChild<SelectPrimitive.TriggerProps> = $props();
</script>

<SelectPrimitive.Trigger bind:ref class={cn(className)} {...restProps}>
	{@render children?.()}
</SelectPrimitive.Trigger>
