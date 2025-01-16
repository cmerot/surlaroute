<script lang="ts" module>
	export type DescriptionProps = WithChildren<WithElementRef<HTMLAttributes<HTMLDivElement>>>;
</script>

<script lang="ts">
	import { cn } from "$lib/utils";
	import type { WithChildren, WithElementRef } from "bits-ui";
	import type { HTMLAttributes } from "svelte/elements";

	let {
		ref = $bindable(null),
		class: className,
		children,
		...restProps
	}: DescriptionProps = $props();
</script>

<div bind:this={ref} class={cn("mb-4 px-4 text-2xl text-foreground/80", className)} {...restProps}>
	{@render children?.()}
</div>
