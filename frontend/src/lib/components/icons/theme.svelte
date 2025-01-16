<script lang="ts" module>
	export type ThemeProps = WithoutChildrenOrChild<SVGAttributes<SVGSVGElement>> & {
		theme: string;
		size?: number | string;
	};
</script>

<script lang="ts">
	import { cn } from "$lib/utils";
	import type { WithoutChildrenOrChild } from "bits-ui";
	import type { SVGAttributes } from "svelte/elements";
	let { class: className, theme, size = 24, ...restProps }: ThemeProps = $props();
</script>

<svg
	width={size}
	height={size}
	viewBox="0 0 24 24"
	xmlns="http://www.w3.org/2000/svg"
	class={cn(`${theme}`, className)}
	{...restProps}
>
	<rect x="0" y="0" width="24" height="24" fill="currentColor" rx="3" ry="3" class="text-primary" />
	<rect
		class="text-secondary"
		x="4"
		y="10"
		width="10"
		height="10"
		fill="currentColor"
		rx="2"
		ry="2"
	/>
</svg>
