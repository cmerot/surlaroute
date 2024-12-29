<script lang="ts" module>
	export type PageProps = WithChildren<WithElementRef<HTMLAttributes<HTMLDivElement>>>;
</script>

<script lang="ts">
	import { cn } from '$lib/utils';
	import type { WithChildren, WithElementRef } from 'bits-ui';
	import type { HTMLAttributes } from 'svelte/elements';

	let { ref = $bindable(null), class: className, children, ...restProps }: PageProps = $props();
</script>

<div bind:this={ref} class={cn('flex h-full flex-col', className)} {...restProps}>
	{@render children?.()}
</div>
