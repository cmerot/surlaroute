<script lang="ts" module>
	export type LogotextProps = WithoutChildrenOrChild<SVGAttributes<SVGSVGElement>> & {
		size?: number | string;
		background?: string;
		title?: string;
	};
</script>

<script lang="ts">
	import type { WithoutChildrenOrChild } from 'bits-ui';
	import type { SVGAttributes } from 'svelte/elements';
	import Logo2 from './logo.svelte';
	let {
		size = 24,
		background = 'none',
		title = 'Sur la route',
		...restProps
	}: LogotextProps = $props();
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	xmlns:xlink="http://www.w3.org/1999/xlink"
	width={size}
	height={size}
	viewBox="0 0 300 300"
	{...restProps}
>
	<circle id="a" cx="-171.62" cy="124.69" r="118.75" fill="none" transform="rotate(-99)" />
	<text>
		<textPath
			xlink:href="#a"
			fill="currentColor"
			style="font-size:38px;font-family:'Marker Aid',marker-aid;"
		>
			{title}
		</textPath>
	</text>
	<Logo2 withText={true} />
</svg>
