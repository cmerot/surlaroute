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

<Marker
	lngLat={lonLngTo2D(feature.geometry.coordinates)}
	offset={[0, -14]}
	class={feature.properties.id === selectedMarkerId ? "z-10" : ""}
>
	<button
		class="marker-container hover:cursor-pointer"
		onclickcapture={(e) => {
			e.stopPropagation();
			toggleSelected(feature.properties.id);
		}}
	>
		<MapPin
			activity={feature.properties.actor_type == "Org"
				? feature.properties.activities[0]
				: undefined}
			size={36}
			selected={feature.properties.id === selectedMarkerId}
		/>
	</button>
</Marker>
