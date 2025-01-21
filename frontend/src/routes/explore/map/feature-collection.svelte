<script lang="ts">
	import type {
		ActorAssocFeatureCollection,
		ActorFeature,
		EventPointFeature,
		TourFeatureCollection,
		TourLineFeature,
	} from "$lib/backend/client";
	import ActorFeatureMarker from "./actor-feature-marker.svelte";
	import EventFeatureMarker from "./event-feature-marker.svelte";
	import TourFeatureLineLayer from "./tour-feature-line-layer.svelte";

	type Props = {
		featureCollection: TourFeatureCollection | ActorAssocFeatureCollection;
		selectedMarkerId?: string;
	};

	let { featureCollection, selectedMarkerId = $bindable() }: Props = $props();

	function isTourFeature(
		feature: TourLineFeature | EventPointFeature | ActorFeature,
	): feature is TourLineFeature {
		return feature.properties.type === "tour_line";
	}

	function isEventFeature(
		feature: TourLineFeature | EventPointFeature | ActorFeature,
	): feature is EventPointFeature {
		return feature.properties.type === "event_point";
	}

	function isActorFeature(
		feature: TourLineFeature | EventPointFeature | ActorFeature,
	): feature is ActorFeature {
		return ["Org", "Person"].includes(feature.properties.type);
	}
</script>

{#each featureCollection.features as feature}
	{#if isTourFeature(feature)}
		<TourFeatureLineLayer {feature} />
	{:else if isActorFeature(feature)}
		<ActorFeatureMarker {feature} bind:selectedMarkerId />
	{:else if isEventFeature(feature)}
		<EventFeatureMarker {feature} bind:selectedMarkerId />
	{/if}
{/each}
