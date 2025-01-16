<script lang="ts">
	import type { ActorAssocPublic, EventPublic, TourPublic } from "$lib/backend/client";
	import { DisciplineBadge } from "$lib/components/discipline-badge";
	import { Mobility, Tour } from "$lib/components/icons";
	import * as Page from "$lib/components/page";
	import Permissions from "$lib/components/permissions/permissions.svelte";
	import { Badge } from "$lib/components/ui/badge";
	import { Button } from "$lib/components/ui/button";
	import * as Card from "$lib/components/ui/card";
	import { onMount } from "svelte";
	import {
		GeoJSON,
		LineLayer,
		MapLibre,
		Marker,
		Popup,
		type LngLatBoundsLike,
	} from "svelte-maplibre";
	import type { PageData } from "./$types";

	type MarkerType = {
		lngLat: [number, number];
		label: string;
		name: string;
		assoc: ActorAssocPublic;
	};

	function getMarkers(events: EventPublic[]): MarkerType[] {
		const markers: Array<MarkerType> = [];
		for (const [event_index, e] of tour.events.entries()) {
			if (e.actor_assocs) {
				for (const assoc of e.actor_assocs) {
					if (assoc.actor?.contact?.address?.geom_point) {
						let label = `${assoc.actor.name} le ${new Date(e.start_dt).toLocaleDateString()}`;

						if (event_index === 0) {
							label = `Départ : ${label}`;
						} else if (event_index < tour.events.length) {
							label = `Étape ${event_index + 1} : ${label}`;
						} else {
							label = `Arrivée : ${label}`;
						}
						markers.push({
							lngLat: assoc.actor.contact.address.geom_point.coordinates as [number, number],
							name: label,
							label,
							assoc,
						});
					}
				}
			}
		}
		return markers;
	}

	function getBoundsFromMarkers(markers: Array<MarkerType>) {
		const bounds = [
			[90, 90], // [lng, lat]
			[-90, -90], // [lng, lat]
		];

		for (const marker of markers) {
			bounds[0][0] = Math.min(bounds[0][0], marker.lngLat[0]); // southwestern lng
			bounds[0][1] = Math.min(bounds[0][1], marker.lngLat[1]); // southwestern lat
			bounds[1][0] = Math.max(bounds[1][0], marker.lngLat[0]); // northeastern lng
			bounds[1][1] = Math.max(bounds[1][1], marker.lngLat[1]); // northeastern lat
		}
		return bounds as LngLatBoundsLike;
	}

	function getProducers(tour: TourPublic) {
		return (
			tour.actor_assocs?.filter((assoc: ActorAssocPublic) => assoc.data?.role === "producer") ?? []
		);
	}

	const { data }: { data: PageData } = $props();
	let map: maplibregl.Map | undefined = $state();
	const tour = data.tour;
	const markers = $derived(getMarkers(tour.events));
	const bounds = $derived(getBoundsFromMarkers(markers));
	const producers = $derived(getProducers(tour));

	onMount(() => {
		if (!map) return;
		map.fitBounds(bounds, {
			padding: {
				top: 100,
				right: 100,
				bottom: 100,
				left: 100,
			},
		});
	});
</script>

<Page.Root>
	<Page.Title Icon={Tour}>{tour.name}</Page.Title>
	<Page.Description class="flex gap-4">
		{tour.year}
		{#each tour.disciplines as discipline}
			<DisciplineBadge {discipline} />
		{/each}
		{#each tour.mobilities as mobility}
			<Mobility {mobility} />
		{/each}
	</Page.Description>
	<Page.Content class="space-y-8">
		<div class="light h-[400px]">
			<MapLibre
				bind:map
				{bounds}
				class="h-full rounded-lg"
				style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
			>
				<GeoJSON id="maine" data={tour.geojson as unknown as string}>
					<LineLayer
						layout={{ "line-cap": "round", "line-join": "round" }}
						paint={{
							"line-width": 5,
							"line-dasharray": [5, 2],
							"line-color": "#008800",
							"line-opacity": 0.8,
						}}
					/>
				</GeoJSON>
				{#each markers as { lngLat, label, name, assoc }, index}
					<!-- <EventMarker {org} event={assoc.event} {step} /> -->
					<Marker
						{lngLat}
						onclick={() => console.log("click")}
						class="grid h-8 w-8 place-items-center"
					>
						<Badge>{index + 1}</Badge>

						<Popup openOn="click" offset={[0, -10]}></Popup>
					</Marker>
				{/each}
			</MapLibre>
		</div>
		<div class="grid gap-6 md:grid-cols-2">
			<Card.Root>
				<Card.Header>
					<Card.Title>À propos</Card.Title>
				</Card.Header>
				<Card.Content class="space-y-4">
					{#if tour.description}
						<p class="prose text-xl">{@html tour.description}</p>
					{/if}
					{#if producers.length > 0}
						<p>
							Produit par {@html producers
								.map((p) => {
									return `<a class="underline" href="/directory/${p.actor.type == "Person" ? "people" : "orgs"}/${p.actor.id}">${p.actor.name}</a>`;
								})
								.join(", ")}
							en {tour.year}
						</p>
					{/if}
				</Card.Content>
			</Card.Root>
			<Card.Root>
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
											href={`/directory/${assoc.actor.type == "Person" ? "people" : "orgs"}/${assoc.actor.id}`}
											class="flex w-full justify-start"
											variant="ghost"
										>
											<div class="w-40">
												{new Date(event.start_dt).toLocaleDateString(undefined, {
													year: "numeric",
													month: "long",
													day: "numeric",
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
		</div>
	</Page.Content>
	<Page.Footer><Permissions entity={tour} /></Page.Footer>
</Page.Root>
