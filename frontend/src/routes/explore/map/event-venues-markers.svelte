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
	<Marker
		lngLat={lonLngTo2D(feature.geometry.coordinates)}
		offset={[0, -14]}
		class={feature.properties.id === selectedMarkerId ? "z-10" : ""}
	>
		<button
			class="marker-container"
			onclickcapture={(e) => {
				e.stopPropagation();
				toggleSelected(feature.properties.id);
			}}
		>
			<MapPin
				activity={event_venue.type == "Org" ? event_venue.activities[0] : undefined}
				size={36}
				selected={feature.properties.id === selectedMarkerId}
			/>
		</button>
	</Marker>
{/each}
