<script lang="ts">
	import type { EventPointFeature } from "$lib/backend/client";
	import { MapPin } from "$lib/components/icons";
	import { Marker } from "svelte-maplibre";
	import { lonLngTo2D } from "../utils";

	type Props = {
		feature: EventPointFeature;
		selectedMarkerId?: string;
	};

	let { feature, selectedMarkerId = $bindable() }: Props = $props();

	function toggleSelected(id: string) {
		selectedMarkerId = selectedMarkerId === id ? undefined : id;
	}
</script>

{#each feature.properties.event_venues as event_venue}
	<Marker lngLat={lonLngTo2D(feature.geometry.coordinates)} offset={[0, -16]}>
		<div class="marker-container hover:cursor-pointer">
			{#if event_venue.type == "Org"}
				<MapPin
					activity={event_venue.activities[0]}
					size={36}
					selected={feature.properties.id === selectedMarkerId}
					onclick={() => {
						toggleSelected(feature.properties.id);
					}}
				/>
			{:else}
				<MapPin
					size={36}
					selected={feature.properties.id === selectedMarkerId}
					onclick={() => {
						toggleSelected(feature.properties.id);
					}}
				/>
			{/if}
		</div>
	</Marker>
{/each}
