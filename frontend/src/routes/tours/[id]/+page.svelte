<script lang="ts">
	import type { ActorAssoc_Explore, EventLitePublic } from '$lib/backend/client';
	import { DisciplineBadge } from '$lib/components/discipline-badge';
	import { Mobility, Tour } from '$lib/components/icons2';
	import * as Page from '$lib/components/page';
	import Permissions from '$lib/components/permissions/permissions.svelte';
	import Badge from '$lib/components/ui/badge/badge.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import * as Table from '$lib/components/ui/table';
	import { onMount } from 'svelte';
	import {
		GeoJSON,
		LineLayer,
		type LngLatBoundsLike,
		MapLibre,
		Marker,
		Popup
	} from 'svelte-maplibre';
	import { type PageData } from './$types';

	type MarkerType = {
		lngLat: [number, number];
		label: string;
		name: string;
		assoc: ActorAssoc_Explore;
	};

	function sortEventsByDate(a: EventLitePublic, b: EventLitePublic) {
		return new Date(a.start_dt).getTime() - new Date(b.start_dt).getTime();
	}

	function getMarkers(events: EventLitePublic[]): MarkerType[] {
		const markers: Array<MarkerType> = [];
		tour.events.forEach((e, event_index) => {
			e.actor_assocs?.forEach((assoc) => {
				if (assoc.actor?.contact?.address?.geom_point) {
					let label = `${assoc.actor.name} le ${new Date(e.start_dt).toLocaleDateString()}`;

					if (event_index === 0) {
						label = `Départ : ${label}`;
					} else if (event_index < tour.events.length) {
						label = `Étape ${event_index + 1} : ${label}`;
					} else {
						label = `Arrivée : ${label}`;
					}
					const m = {
						lngLat: assoc.actor.contact.address.geom_point.coordinates as [number, number],
						name: label,
						label,
						assoc
					};
					markers.push(m);
				}
			});
		});
		return markers;
	}

	function getBoundsFromMarkers(markers: Array<MarkerType>) {
		let bounds = [
			[90, 90], // [lng, lat]
			[-90, -90] // [lng, lat]
		];

		markers.forEach((marker) => {
			bounds[0][0] = Math.min(bounds[0][0], marker.lngLat[0]); // southwestern lng
			bounds[0][1] = Math.min(bounds[0][1], marker.lngLat[1]); // southwestern lat
			bounds[1][0] = Math.max(bounds[1][0], marker.lngLat[0]); // northeastern lng
			bounds[1][1] = Math.max(bounds[1][1], marker.lngLat[1]); // northeastern lat
		});
		return bounds as LngLatBoundsLike;
	}

	const { data }: { data: PageData } = $props();

	const { tour, geojson } = data;

	let map: maplibregl.Map | undefined = $state();

	tour.events.sort(sortEventsByDate);
	const markers = getMarkers(tour.events);
	const bounds = getBoundsFromMarkers(markers);

	onMount(() => {
		if (!map) return;
		map.fitBounds(bounds, { padding: { top: 100, right: 100, bottom: 100, left: 100 } });
	});
	const { disciplines, mobilities } = tour;
</script>

<Page.Root>
	<Page.Title class="flex items-center" Icon={Tour}>
		<span class="grow">{tour.name} </span>
	</Page.Title>
	<Page.Description class="flex gap-4">
		{tour.year}
		{#each tour.disciplines as discipline}
			<DisciplineBadge {discipline} />
		{/each}
		{#each tour.mobilities as mobility}
			<Mobility {mobility} />
		{/each}
	</Page.Description>
	<Page.Content>
		{#if markers.length > 0}
			<div class="light h-[400px]">
				<MapLibre
					bind:map
					{bounds}
					class="h-full"
					style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
				>
					<GeoJSON id="maine" data={geojson as unknown as string}>
						<LineLayer
							layout={{ 'line-cap': 'round', 'line-join': 'round' }}
							paint={{
								'line-width': 5,
								'line-dasharray': [5, 2],
								'line-color': '#008800',
								'line-opacity': 0.8
							}}
						/>
					</GeoJSON>
					{#each markers as { lngLat, label, name, assoc }, index}
						<!-- <EventMarker {org} event={assoc.event} {step} /> -->
						<Marker
							{lngLat}
							onclick={() => console.log('click')}
							class="grid h-8 w-8 place-items-center"
						>
							<Badge>{index + 1}</Badge>

							<Popup openOn="click" offset={[0, -10]}></Popup>
						</Marker>
					{/each}
				</MapLibre>
			</div>
		{/if}
		<Card.Root class="mt-8">
			<Card.Header>
				<Card.Title>Dates</Card.Title>
			</Card.Header>
			<Card.Content class="p-2">
				{#each tour.events as event, event_index}
					{#if event.actor_assocs}
						<ul>
							{#each event.actor_assocs as assoc}
								<li>
									<Button
										href={`/directory/${assoc.actor.type == 'Person' ? 'people' : 'orgs'}/${assoc.actor.id}`}
										class="flex w-full justify-start"
										variant="ghost"
									>
										<div class="w-40">
											{new Date(event.start_dt).toLocaleDateString(undefined, {
												year: 'numeric',
												month: 'long',
												day: 'numeric'
											})}
										</div>
										<Badge>{event_index + 1}</Badge>
										{assoc.actor.name}
									</Button>
								</li>
							{/each}
						</ul>
					{/if}
				{/each}
			</Card.Content>
		</Card.Root>

		<Card.Root class="mt-8">
			<Card.Header>
				<Card.Title>Contacts</Card.Title>
			</Card.Header>
			<Card.Content class="p-2">
				{#if tour.actor_assocs}
					<ul>
						{#each tour.actor_assocs as assoc}
							<li>
								<Button
									variant="ghost"
									class="block"
									href={`/directory/${assoc.actor.type == 'Person' ? 'people' : 'orgs'}/${assoc.actor.id}`}
								>
									{assoc.actor.name}
									{#if assoc.data?.role}
										({assoc.data.role})
									{/if}
								</Button>
							</li>
						{/each}
					</ul>
				{/if}
			</Card.Content>
		</Card.Root>
	</Page.Content>
	<Page.Footer>
		<Permissions entity={tour} />
	</Page.Footer>
</Page.Root>
