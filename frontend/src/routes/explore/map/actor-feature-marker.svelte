<script lang="ts">
	import type { ActorFeature } from "$lib/backend/client";
	import { MapPin } from "$lib/components/icons";
	import { Marker } from "svelte-maplibre";
	import { lonLngTo2D } from "../utils";

	type Props = {
		feature: ActorFeature;
		selectedMarkerId?: string;
	};

	let { feature, selectedMarkerId = $bindable() }: Props = $props();

	function toggleSelected(id: string) {
		selectedMarkerId = selectedMarkerId === id ? undefined : id;
	}
</script>

<Marker lngLat={lonLngTo2D(feature.geometry.coordinates)} offset={[0, -16]}>
	<div class="marker-container hover:cursor-pointer">
		{#if feature.properties.type == "Org"}
			<MapPin
				activity={feature.properties.activities[0]}
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
