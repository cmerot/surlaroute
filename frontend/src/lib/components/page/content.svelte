<script lang="ts" module>
	export type ContentProps = WithChildren<WithElementRef<HTMLAttributes<HTMLDivElement>>>;
</script>

<script lang="ts">
	import { cn } from "$lib/utils";
	import type { WithChildren, WithElementRef } from "bits-ui";
	import type { HTMLAttributes } from "svelte/elements";

	let { ref = $bindable(null), class: className, children, ...restProps }: ContentProps = $props();
</script>

<div bind:this={ref} class={cn("flex-grow p-4", className)} {...restProps}>
	{@render children?.()}
</div>
