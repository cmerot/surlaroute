<script lang="ts">
	import type { TourFeatureCollection as TourFeatureCollectionType } from "$lib/backend/client";
	import { bbox } from "@turf/turf";

	import type { Feature, Polygon } from "geojson";
	import { ChevronLeft } from "lucide-svelte";
	import { type Map as MapLibreGLMap } from "maplibre-gl";
	import { onMount } from "svelte";
	import type { LngLatBoundsLike, LngLatLike } from "svelte-maplibre";
	import Filters from "./map-info/filters.svelte";
	import MapInfo from "./map-info/map-info.svelte";
	import Map from "./map/map.svelte";
	import TourFeatureCollection from "./map/tour-feature-collection.svelte";

	type Props = {
		map: MapLibreGLMap | undefined;
		center?: LngLatLike | undefined;
		zoom?: number | undefined;
		bounds?: LngLatBoundsLike | undefined;
		searchInBounds?: boolean;
		mobilityPath?: string | undefined;
		featureCollections: TourFeatureCollectionType[];
		selectedMarkerId?: string | undefined;
		selectedTourId?: string | undefined;
		polygon?: Feature<Polygon>;
	};

	let {
		map = $bindable(),
		center = $bindable(),
		zoom = $bindable(),
		bounds = $bindable(),
		searchInBounds = $bindable(false),
		mobilityPath = $bindable(),
		selectedTourId = $bindable(),
		selectedMarkerId = $bindable(),
		polygon = $bindable(),
		featureCollections,
	}: Props = $props();

	let showActors: boolean | undefined = $state();
	let newTourSelected = $state(false);
	let newMarkerSelected: boolean = $state(false);

	/**
	 * Open the sidebar when a tour or a marker is selected
	 */
	$effect(() => {
		if (selectedMarkerId || selectedTourId) {
			isOpen = true;
		}
	});

	/**
	 * Track when a new marker is selected
	 */
	$effect(() => {
		newMarkerSelected = !!selectedMarkerId;
	});

	/**
	 * Pan to the marker when it is newly selected and outside of the viewport
	 */
	$effect(() => {
		if (!selectedMarkerId || !newMarkerSelected || !map) {
			return;
		}
		newMarkerSelected = false;

		const feature = featureCollections
			.flatMap((c) => c.features)
			.find((f) => f.properties.id === selectedMarkerId);

		if (!feature) return;

		const mapBounds = map.getBounds();
		let sw = mapBounds.getSouthWest();
		const pixels = map.project(sw);
		pixels.x = pixels.x + 312;
		sw = map.unproject(pixels);
		mapBounds.setSouthWest(sw);

		if (!mapBounds.contains(feature.geometry.coordinates as LngLatLike)) {
			map.panTo(feature.geometry.coordinates as LngLatLike);
		}
	});

	/**
	 * Select the tour from the selectedMarkerId
	 */
	$effect(() => {
		if (selectedMarkerId) {
			const tour = featureCollections.find((collection) =>
				collection.features.some((feature) => feature.properties.id === selectedMarkerId),
			);
			if (tour) {
				selectedTourId = tour.properties.id;
			}
		}
	});

	/**
	 * Track when a new tour is selected
	 */
	$effect(() => {
		newTourSelected = !!selectedTourId;
	});

	/**
	 * Fit bounds to a tour when newly selected
	 */
	$effect(() => {
		if (!selectedTourId || !newTourSelected || !map) {
			return;
		}
		newTourSelected = false;
		// selectedMarkerId = undefined;

		const collection = featureCollections.find(
			(collection) => collection.properties.id === selectedTourId,
		);
		if (collection) {
			if (selectedMarkerId) {
				const markerBelongsToCollection = collection.features.some(
					(feature) => feature.properties.id === selectedMarkerId,
				);
				if (!markerBelongsToCollection) {
					selectedMarkerId = undefined;
				}
			}
			const filteredCollection = {
				...collection,
				features: collection.features.filter(
					(feature) => feature.properties.type === "event_point",
				),
			};
			map.fitBounds(bbox(filteredCollection as unknown as Feature) as LngLatBoundsLike);
		}
	});

	let isOpen = $state(false);

	onMount(() => {
		if (!map) return;
		map.on("click", () => {
			// isOpen = false;
			selectedMarkerId = undefined;
			selectedTourId = undefined;
		});
	});
</script>

<div class="relative flex h-[calc(100svh-4rem)]">
	<div
		class="absolute bottom-0 left-0 top-0 z-40 w-72 bg-background transition-all duration-300 ease-in-out {isOpen
			? 'translate-x-0'
			: '-translate-x-full'}"
	>
		<button
			class="absolute right-[-1.5rem] top-[calc(50%-1.5rem/2)] h-12 rounded-r bg-background text-foreground shadow"
			onclick={() => {
				isOpen = !isOpen;
			}}
		>
			<ChevronLeft class="size-6 {!isOpen ? 'rotate-180' : ''} transition-transform duration-300" />
		</button>
		<MapInfo
			class="relative shadow"
			bind:selectedTourId
			bind:selectedMarkerId
			bind:showActors
			tourFeatureCollections={featureCollections}
		/>
	</div>
	<Map class="grow" bind:map bind:bounds bind:center bind:zoom>
		<Filters
			bind:mobilityPath
			bind:searchInBounds
			class="transition-translate absolute left-72 z-50 flex-nowrap gap-4 overflow-x-auto p-4 duration-300 ease-in-out md:flex {isOpen
				? 'hidden translate-x-0'
				: 'flex -translate-x-[288px]'}"
		/>
		{#each featureCollections as feactureCollection}
			<TourFeatureCollection
				featureCollection={feactureCollection}
				bind:selectedMarkerId
				{showActors}
			/>
		{/each}
	</Map>
</div>
