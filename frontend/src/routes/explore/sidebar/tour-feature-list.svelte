<script lang="ts">
	import type {
		EventPointFeatureProperties,
		OrgFeatureProperties,
		PersonFeatureProperties,
		TourFeatureCollection,
	} from "$lib/backend/client";
	import { DisciplineBadge } from "$lib/components/discipline-badge";
	import { Activity, Directory, Mobility, Person } from "$lib/components/icons";
	import * as Accordion from "$lib/components/ui/accordion";
	import { Button } from "$lib/components/ui/button";
	import * as Tabs from "$lib/components/ui/tabs";
	import AccordionTrigger from "./accordion-trigger.svelte";

	type Props = {
		selectedTourId?: string;
		selectedMarkerId?: string;
		tours: TourFeatureCollection[];
		showActors?: boolean;
	};

	let {
		tours: results,
		selectedTourId = $bindable(),
		selectedMarkerId = $bindable(),
		showActors = $bindable(),
	}: Props = $props();

	function isSelectedTour(id: string) {
		return id === selectedTourId;
	}

	function isSelectedMarker(id: string) {
		return id === selectedMarkerId;
	}

	/**
	 * Reset selected event id when tour is unselected
	 */
	$effect(() => {
		if (!selectedTourId || selectedMarkerId == "") {
			selectedMarkerId = undefined;
		}
	});

	let tours = $derived.by(() =>
		results.map((tourFeatureCollection) => {
			const events = tourFeatureCollection.features
				.filter((feature) => feature.properties.type === "event_point")
				.map((event) => event.properties) as Array<EventPointFeatureProperties>;

			const actors = tourFeatureCollection.features
				.filter((feature) => feature.properties.type === "tour_actor")
				.map((actor) => actor.properties) as Array<OrgFeatureProperties | PersonFeatureProperties>;

			return {
				...tourFeatureCollection.properties,
				events,
				actors,
			};
		}),
	);

	let value: string = $state("events");

	$effect(() => {
		showActors = value === "actors";
	});
</script>

<Accordion.Root type="single" bind:value={selectedTourId}>
	{#each tours as tour}
		<Accordion.Item value={tour.id}>
			<AccordionTrigger
				class="border-b border-secondary/50 p-4 text-left hover:bg-secondary/50 {isSelectedTour(
					tour.id,
				)
					? 'bg-secondary/50'
					: ''}"
			>
				<div class="flex w-full items-center justify-between">
					<span>
						{tour.name}
					</span>
					<span class="flex gap-2">
						{tour.year}
						{#each tour.disciplines as discipline}
							<DisciplineBadge {discipline} />
						{/each}
						{#each tour.mobilities as mobility}
							<Mobility {mobility} class="inline" />
						{/each}
					</span>
				</div>
				<div>
					<small class="text-muted-foreground">
						{#each tour.producers as producer}
							<span class="inline-block">
								{producer.name}
							</span>
						{/each}
					</small>
				</div>
			</AccordionTrigger>
			<Accordion.Content class="space-y-4 p-4">
				<Tabs.Root bind:value>
					<Tabs.List>
						<Tabs.Trigger value="events">Dates</Tabs.Trigger>
						<Tabs.Trigger value="actors">Ressources</Tabs.Trigger>
					</Tabs.List>
					<Tabs.Content value="events" class="space-y-2">
						{#each tour.events as event}
							{#each event.event_venues as actor}
								<div class="flex gap-2">
									<Button
										class=" grow space-x-2 overflow-hidden {isSelectedMarker(event.id)
											? ' outline outline-2'
											: ''}"
										variant="ghost"
										onclick={() => {
											if (isSelectedMarker(event.id)) selectedMarkerId = undefined;
											else selectedMarkerId = event.id;
										}}
									>
										<span>
											{new Date(event.start_dt).toLocaleDateString(undefined, {
												year: "numeric",
												month: "2-digit",
												day: "2-digit",
											})}
										</span>
										<span class="min-w-0 flex-grow truncate text-left">
											<span class="">{actor.name}</span>
										</span>
									</Button>
									<Button
										href={`/directory/${actor.type == "Person" ? "people" : "orgs"}/${actor.id}`}
										variant="secondary"
									>
										<Directory size={6} />
									</Button>
								</div>
							{/each}
						{/each}
					</Tabs.Content>
					<Tabs.Content value="actors" class="space-y-2">
						{#each tour.actors as actor}
							<div class="flex gap-2">
								<Button
									class=" grow overflow-hidden {isSelectedMarker(actor.id)
										? ' outline outline-2'
										: ''}"
									variant="ghost"
									onclick={() => {
										if (isSelectedMarker(actor.id)) selectedMarkerId = undefined;
										else selectedMarkerId = actor.id;
									}}
								>
									<span class="min-w-0 flex-grow truncate text-left">
										{#if actor.actor_type == "Org"}
											<Activity size={6} activity={actor.activities[0]} class="inline" />
										{:else}
											<Person size={6} />
										{/if}
										<span class="">{actor.name}</span>
									</span>
								</Button>
								<Button
									href={`/directory/${actor.actor_type == "Person" ? "people" : "orgs"}/${actor.id}`}
									variant="secondary"
								>
									<Directory size={6} />
								</Button>
							</div>
						{/each}
					</Tabs.Content>
				</Tabs.Root>
			</Accordion.Content>
		</Accordion.Item>
	{/each}
</Accordion.Root>
