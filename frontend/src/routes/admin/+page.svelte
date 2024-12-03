<script lang="ts">
	import type { LngLat, MapMouseEvent } from 'maplibre-gl';
	import { DefaultMarker, MapEvents, MapLibre } from 'svelte-maplibre';

	let markers: { lngLat: LngLat }[] = $state([]);

	function addMarker(e: MapMouseEvent) {
		console.log(e.lngLat);
		markers = [...markers, { lngLat: e.lngLat }];
	}
</script>

<MapLibre
	center={[8.442194600786223, 46.89462538131045]}
	zoom={5}
	class="h-full"
	style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
>
	<MapEvents onclick={addMarker} />

	{#each markers as marker}
		<DefaultMarker lngLat={marker.lngLat} />
	{/each}
</MapLibre>
