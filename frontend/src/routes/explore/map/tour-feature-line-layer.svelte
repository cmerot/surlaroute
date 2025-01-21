<script lang="ts">
	import type { TourLineFeature } from "$lib/backend/client";
	import { GeoJSON, LineLayer } from "svelte-maplibre";

	type Props = {
		feature: TourLineFeature;
	};

	let { feature }: Props = $props();
</script>

<GeoJSON data={feature as unknown as string}>
	<LineLayer
		layout={{ "line-cap": "round", "line-join": "round" }}
		paint={{
			"line-width": 3,
			"line-color": "#b696c6",
		}}
	/>
</GeoJSON>
