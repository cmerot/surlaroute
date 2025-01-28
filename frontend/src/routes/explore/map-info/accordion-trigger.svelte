<script lang="ts">
	import { cn } from "$lib/utils.js";
	import { Accordion as AccordionPrimitive, type WithoutChild } from "bits-ui";

	let {
		ref = $bindable(null),
		class: className,
		level = 3,
		children,
		...restProps
	}: WithoutChild<AccordionPrimitive.TriggerProps> & {
		level?: AccordionPrimitive.HeaderProps["level"];
	} = $props();
</script>

<AccordionPrimitive.Header {level} class="flex">
	<AccordionPrimitive.Trigger
		bind:ref
		class={cn("w-full transition-all", className)}
		{...restProps}
	>
		{@render children?.()}
	</AccordionPrimitive.Trigger>
</AccordionPrimitive.Header>
