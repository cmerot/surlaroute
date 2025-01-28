<script lang="ts">
	import { goto } from "$app/navigation";
	import { page } from "$app/state";
	import type { LngLatBoundsLike, Map as MapLibreGLMap } from "maplibre-gl";
	import { LngLatBounds } from "maplibre-gl";

	import { onMount } from "svelte";
	import type { PageData } from "./$types";
	import ExploreMapMd from "./explore.svelte";
	import { parseUrlSearch } from "./utils";

	const { data }: { data: PageData } = $props();

	let map: MapLibreGLMap | undefined = $state();
	let bounds: LngLatBoundsLike | LngLatBounds = $state(data.query.bounds);
	let mobilityPath: string | undefined = $state(data.query.m);
	let centerParam: string | undefined = $state();
	let boundsParam: string | undefined = $state();
	let searchInBounds: boolean = $state(false);
	let selectedTourId: string | undefined = $state();
	let selectedMarkerId: string | undefined = $state();

	/**
	 * Persists state to the URL
	 */
	$effect(() => {
		const params: string[] = [];
		if (centerParam) params.push(`@${centerParam}`);
		if (searchInBounds && boundsParam) params.push(`b=${boundsParam}`);
		if (mobilityPath) params.push(`m=${mobilityPath}`);
		if (selectedMarkerId) params.push(`sm=${selectedMarkerId}`);
		else if (selectedTourId) params.push(`st=${selectedTourId}`);

		if (params.length < 1) return;
		goto(`?${params.join("&")}`, {
			keepFocus: true,
			invalidateAll: false,
			replaceState: false,
		});
	});

	onMount(() => {
		selectedMarkerId = page.url.searchParams.get("sm") || undefined;
		selectedTourId = page.url.searchParams.get("st") || undefined;
		if (!map) return;

		map!.setPadding({ left: 330, right: 60, top: 60, bottom: 24 });

		const mapPosition = parseUrlSearch(page.url.search);

		if (mapPosition) {
			const { lat, lon, zoom } = mapPosition;
			map.setCenter([lon, lat]);
			map.setZoom(zoom);
		}

		map.on("moveend", () => {
			const mapCenter = map!.getCenter();
			const zoom = map!.getZoom();
			centerParam = [mapCenter.lat.toFixed(3), mapCenter.lng.toFixed(3), zoom.toFixed(1)].join(",");
			const mapBounds = map!.getBounds();
			boundsParam = mapBounds
				.toArray()
				.flat()
				.map((n) => n.toFixed(3))
				.join(",");
		});
	});
</script>

<ExploreMapMd
	bind:map
	bind:bounds
	bind:searchInBounds
	bind:mobilityPath
	bind:selectedMarkerId
	bind:selectedTourId
	featureCollections={data.results.slr}
/>
