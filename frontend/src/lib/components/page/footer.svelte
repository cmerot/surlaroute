<script lang="ts" module>
	export type FooterProps = WithChildren<WithElementRef<HTMLAttributes<HTMLDivElement>>>;
</script>

<script lang="ts">
	import { cn } from '$lib/utils';
	import type { WithChildren, WithElementRef } from 'bits-ui';
	import type { HTMLAttributes } from 'svelte/elements';

	let { ref = $bindable(null), class: className, children, ...restProps }: FooterProps = $props();
</script>

<div bind:this={ref} class={cn('bg-background p-4', className)} {...restProps}>
	{@render children?.()}
</div>
