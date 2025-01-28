<script lang="ts">
	import type {
		ActorFeature,
		EventPointFeature,
		TourFeatureCollection,
		TourLineFeature,
	} from "$lib/backend/client";
	import ActorFeatureMarker from "./actor-feature-marker.svelte";
	import EventFeatureMarker from "./event-venues-markers.svelte";
	import TourFeatureLineLayer from "./tour-feature-line-layer.svelte";

	type Props = {
		featureCollection: TourFeatureCollection;
		selectedMarkerId?: string;
		showActors?: boolean;
	};

	let { featureCollection, selectedMarkerId = $bindable(), showActors }: Props = $props();

	function isTourFeature(
		feature: TourLineFeature | EventPointFeature | ActorFeature,
	): feature is TourLineFeature {
		return feature.properties.type === "tour_line";
	}

	function isEventPointFeature(
		feature: TourLineFeature | EventPointFeature | ActorFeature,
	): feature is EventPointFeature {
		return feature.properties.type === "event_point";
	}

	function isActorFeature(
		feature: TourLineFeature | EventPointFeature | ActorFeature,
	): feature is ActorFeature {
		return ["tour_actor", "event_actor"].includes(feature.properties.type);
	}
</script>

{#each featureCollection.features as feature}
	{#if isTourFeature(feature)}
		<TourFeatureLineLayer {feature} />
	{:else if isActorFeature(feature) && showActors}
		<ActorFeatureMarker {feature} bind:selectedMarkerId />
	{:else if isEventPointFeature(feature) && !showActors}
		<EventFeatureMarker {feature} bind:selectedMarkerId />
	{/if}
{/each}
