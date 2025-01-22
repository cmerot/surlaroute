<script lang="ts">
	import { goto } from "$app/navigation";
	import { bbox } from "@turf/bbox";
	import type {
		LngLat,
		LngLatBoundsLike,
		LngLatLike,
		Map as MaplibreMap,
		StyleSpecification,
	} from "maplibre-gl";
	import { LngLatBounds } from "maplibre-gl";
	import { mode } from "mode-watcher";
	import { onMount } from "svelte";
	import { MapLibre } from "svelte-maplibre";
	import type { PageData } from "./$types";
	import Controls from "./map/controls.svelte";
	import { getStyleName, styles, type Styles } from "./map/styles";
	import TourFeatureCollection from "./map/tour-feature-collection.svelte";
	import Sidebar from "./sidebar/sidebar.svelte";
	import { boundsTo2D, isLngLatBounds } from "./utils";

	const { data }: { data: PageData } = $props();

	let mapInstance: MaplibreMap | undefined = $state();
	let styleName: keyof Styles = $state(getStyleName($mode));
	let style: string | StyleSpecification = $state(styles[getStyleName($mode)].style);
	let bounds: LngLatBoundsLike | LngLatBounds = $state(boundsTo2D(data.query.geo.bounds));
	let center: LngLatLike | undefined = $state(data.query.geo.center);
	let zoom: number | undefined = $state(data.query.geo.center?.zoom);
	let mobilityPath: string | undefined = $state(data.query.m);

	/**
	 * Update map style from the select component
	 */
	$effect(() => {
		style = styles[styleName].style;
	});

	/**
	 * Update the bounds string from the bounds object,
	 * used to update the URL search params and bind api requests
	 */
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	let boundsString: string | undefined = $derived.by(() => {
		if (isLngLatBounds(bounds)) {
			return [
				bounds.getWest().toFixed(7),
				bounds.getSouth().toFixed(7),
				bounds.getEast().toFixed(7),
				bounds.getNorth().toFixed(7),
			].join(",");
		}
	});

	/**
	 * Update the center string from the center object and zoom,
	 */
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	let centerString: string | undefined = $derived.by(() => {
		if (center && zoom) {
			return (
				[
					(center as LngLat).lng.toFixed(7),
					(center as LngLat).lat.toFixed(7),
					zoom.toFixed(2),
				].join(",") + "z"
			);
		}
	});

	/**
	 * Sidebar search input, selected tour id and selected marker id
	 */
	let q: string | undefined = $state();
	let selectedTourId: string | undefined = $state();
	let selectedMarkerId: string | undefined = $state();

	/**
	 * Fit bounds to a tour when selected
	 */
	$effect(() => {
		if (!selectedTourId || !mapInstance) return;

		const tourFeatureCollection = data.results.slr.find(
			(tourFeactureCollection) => tourFeactureCollection.properties.id == selectedTourId,
		);
		if (tourFeatureCollection) {
			// @ts-expect-error: tour_feature_collection is ensured to match GeoJSON.FeatureCollection
			mapInstance.fitBounds(bbox(tourFeatureCollection), {
				padding: { left: 484, right: 100, top: 100, bottom: 100 },
			});
		}
	});

	/**
	 * Pan to marker when marker is selected
	 */
	$effect(() => {
		if (!selectedMarkerId || !mapInstance) return;
		for (const tourFeatureCollection of data.results.slr) {
			const feature = tourFeatureCollection.features.find(
				(feature) => feature.properties.id == selectedMarkerId,
			);
			if (feature) {
				mapInstance.panTo(feature.geometry.coordinates as LngLatLike, {
					padding: { left: 484, right: 100, top: 100, bottom: 100 },
				});
				return;
			}
		}
	});

	/**
	 * Persists state to the URL
	 */
	$effect(() => {
		const params: string[] = [];
		// if (centerString) params.push(`c=${centerString}`);
		// if (boundsString) params.push(`b=${boundsString}`);
		if (q) params.push(`q=${q}`);
		if (mobilityPath) params.push(`m=${mobilityPath}`);
		// if (selectedTourId) params.push(`e=${selectedTourId}&t=Tour`);
		goto(`?${params.join("&")}`, {
			keepFocus: true,
			replaceState: false,
		});
	});

	onMount(() => {
		if (mapInstance && bounds) {
			mapInstance.fitBounds(bounds, { padding: { left: 394, right: 10, top: 10, bottom: 10 } });
		}
	});

	let showActors: boolean | undefined = $state();
</script>

<div class="relative h-full w-full">
	<MapLibre class="h-full w-full overflow-auto" {style} bind:map={mapInstance}>
		<Controls bind:styleName />
		{#each data.results.slr as tourFeactureCollection}
			<TourFeatureCollection
				featureCollection={tourFeactureCollection}
				bind:selectedMarkerId
				{showActors}
			/>
		{/each}
	</MapLibre>
	<Sidebar
		class="absolute left-0 top-0 z-50 max-h-full w-96"
		bind:q
		bind:selectedTourId
		bind:selectedMarkerId
		bind:showActors
		bind:mobilityPath
		apiResults={data.results}
	/>
</div>
