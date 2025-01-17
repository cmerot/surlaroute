<script lang="ts" module>
	export type LogoProps = WithoutChildrenOrChild<SVGAttributes<SVGSVGElement>> & {
		size?: number | string;
		withText?: boolean;
		background?: string;
		activity?: TreePublic;
	};
</script>

<script lang="ts">
	import type { TreePublic } from "$lib/backend/client";
	import type { WithoutChildrenOrChild } from "bits-ui";
	import type { SVGAttributes } from "svelte/elements";
	import Activity from "./activity.svelte";

	let { size = 24, activity, ...restProps }: LogoProps = $props();

	type SizeProps = {
		width?: number | string;
		height?: number | string;
	};

	const sizeProps: SizeProps = $state({ width: size, height: size });
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	viewBox="0 0 24 24"
	fill="#b696c6"
	stroke="#b696c6"
	stroke-width="1"
	stroke-linecap="round"
	stroke-linejoin="round"
	{...restProps}
	{...sizeProps}
>
	<path
		d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"
	/>
	{#if activity}
		<Activity {activity} size="10" x="7" y="5" class="text-white" />
	{/if}
</svg>
