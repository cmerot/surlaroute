<script lang="ts" module>
	export type LogoProps = WithoutChildrenOrChild<SVGAttributes<SVGSVGElement>> & {
		size?: number | string;
		withText?: boolean;
		background?: string;
		activity?: TreePublic;
		selected?: boolean;
	};
</script>

<script lang="ts">
	import type { TreePublic } from "$lib/backend/client";
	import type { WithoutChildrenOrChild } from "bits-ui";
	import clsx from "clsx";
	import type { SVGAttributes } from "svelte/elements";
	import Activity from "./activity.svelte";

	let { size = 24, activity, selected, class: classNames, ...restProps }: LogoProps = $props();

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
	stroke="#7b6191"
	stroke-width="1.5"
	stroke-linecap="round"
	stroke-linejoin="round"
	class={clsx(`origin-bottom transition-transform ${selected ? "scale-150" : ""}`, classNames)}
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
