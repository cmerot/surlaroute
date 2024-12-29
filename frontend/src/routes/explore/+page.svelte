<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as Drawer from '$lib/components/ui/drawer/index.js';
	import * as Table from '$lib/components/ui/table';
	import { DefaultMarker, type LngLatBoundsLike, MapLibre, Popup } from 'svelte-maplibre';
	import { type PageData } from './$types';
	import DrawerOverlay from './dialog-overlay.svelte';
	// const { data: tour }: { data: PageData } = $props();
	type MarkerType = {
		lngLat: [number, number];
		label: string;
		name: string;
	};
	// const markers: Array<MarkerType> = [];

	const markers = $state<Array<MarkerType>>([]);

	// $effect(() => {
	// 	tour.events.sort((a, b) => new Date(a.start_dt).getTime() - new Date(b.start_dt).getTime());
	// 	tour.events.forEach((e, i) => {
	// 		e.actor_assocs.forEach((a) => {
	// 			if (a.actor?.contact?.address?.geom_point) {
	// 				let label = `${a.actor.name} le ${new Date(e.start_dt).toLocaleDateString()}`;

	// 				if (i === 0) {
	// 					label = `Départ #${i + 1} : ${label}`;
	// 				} else if (i === tour.events.length - 1) {
	// 					label = `Arrivée #${i + 1} : ${label}`;
	// 				} else {
	// 					label = `Étape ${i + 1} : ${label}`;
	// 				}
	// 				const m = {
	// 					lngLat: a.actor.contact.address.geom_point.coordinates as [number, number],
	// 					name: label,
	// 					label
	// 				};
	// 				markers.push(m);
	// 			}
	// 		});
	// 	});
	// });

	// function getBoundsFromMarkers(markers: Array<MarkerType>) {
	// 	let bounds = [
	// 		[90, 90], // [lng, lat]
	// 		[-90, -90] // [lng, lat]
	// 	];

	// 	markers.forEach((marker) => {
	// 		bounds[0][0] = Math.min(bounds[0][0], marker.lngLat[0]); // southwestern lng
	// 		bounds[0][1] = Math.min(bounds[0][1], marker.lngLat[1]); // southwestern lat
	// 		bounds[1][0] = Math.max(bounds[1][0], marker.lngLat[0]); // northeastern lng
	// 		bounds[1][1] = Math.max(bounds[1][1], marker.lngLat[1]); // northeastern lat
	// 	});
	// 	return bounds as LngLatBoundsLike;
	// }

	// const bounds = $derived(getBoundsFromMarkers(markers));

	// function doSomething(map) {
	// 	console.log('fitBounds');
	// 	map.fitBounds(bounds, { padding: { top: 100, right: 100, bottom: 100, left: 100 } });
	// }
</script>

<div>
	<!-- <MapLibre style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"> -->
	<!-- {#snippet children({ map })}
        {#each markers as { lngLat, name }}
					<DefaultMarker {lngLat} draggable>
						<Popup offset={[0, -10]}>
							<div class="text-lg font-bold">{name}</div>
						</Popup>
                        </DefaultMarker>
                        {/each}
			{/snippet} -->
	<!-- </MapLibre> -->

	<Drawer.Root>
		<Drawer.Trigger>Open</Drawer.Trigger>
		<Drawer.Portal disabled={true} />
		<DrawerOverlay />

		<Drawer.Content>
			<Drawer.Header>
				<Drawer.Title>Are you sure absolutely sure?</Drawer.Title>
				<Drawer.Description>This action cannot be undone.</Drawer.Description>
			</Drawer.Header>
			<Drawer.Footer>
				<Button>Submit</Button>
				<Drawer.Close>Cancel</Drawer.Close>
			</Drawer.Footer>
		</Drawer.Content>
	</Drawer.Root>
</div>
