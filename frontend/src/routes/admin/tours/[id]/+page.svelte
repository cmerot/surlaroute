<script lang="ts">
	import type { OrgPublic } from '$lib/backend/client';
	import Events from '$lib/components/events.svelte';
	import Orgs from '$lib/components/orgs.svelte';
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import { type PageData } from './$types';

	const { data: tour }: { data: PageData } = $props();
	let ressources: OrgPublic[] = $state([]);
	const ressources_assoc =
		tour.actor_assocs?.filter((assoc) => {
			console.log(assoc.actor.type);
			return assoc.actor.type === 'Org';
		}) || [];

	const diffusions = $derived(tour.events?.map((e) => e.event_venue) || []);
	// console.log(tour.events?.map((e) => e.event_venue));
	// $effect(() => {
	// 	// ressources = ressources_assoc?.map((assoc) => assoc.actor);
	// 	// console.log(ressources);
	// });
</script>

<h1>{tour.name}</h1>

<Tabs.Root value="ressources">
	<Tabs.List class="grid w-full grid-cols-4">
		<Tabs.Trigger value="events">Événements</Tabs.Trigger>
		<Tabs.Trigger value="diffusions">Lieux de diff</Tabs.Trigger>
		<Tabs.Trigger value="ressources">Ressources</Tabs.Trigger>
		<Tabs.Trigger value="people">Contacts</Tabs.Trigger>
	</Tabs.List>
	<Tabs.Content value="events">
		{#if tour.events?.length}
			<Events events={tour.events} />
		{/if}
	</Tabs.Content>
	<Tabs.Content value="diffusions">
		<Orgs orgs={diffusions} />
	</Tabs.Content>
	<Tabs.Content value="ressources">
		<Orgs orgs={ressources} />
	</Tabs.Content>
	<Tabs.Content value="people"></Tabs.Content>
</Tabs.Root>
