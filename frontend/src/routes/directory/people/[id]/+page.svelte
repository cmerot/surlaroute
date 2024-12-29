<script lang="ts">
	import ContactBar from '$lib/components/directory/contact-bar.svelte';
	import Contact from '$lib/components/directory/contact.svelte';
	import PersonOrganisations from '$lib/components/directory/page/person-organisations.svelte';
	import { Org, Person } from '$lib/components/icons2';
	import * as Page from '$lib/components/page';
	import Permissions from '$lib/components/permissions/permissions.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { onMount } from 'svelte';
	import { type PageData } from './$types';

	const { data: person }: { data: PageData } = $props();

	const description: string[] = $state([]);
	onMount(() => {
		if (person.role) {
			description.push(person.role);
		}
		if (person.contact?.address?.q) {
			description.push(person.contact.address.q);
		}
	});
</script>

<Page.Root>
	<Page.Title Icon={Person}>{person.name}</Page.Title>
	{#if description.length > 0}
		<Page.Description>
			{description.join(', ')}
		</Page.Description>
	{/if}
	<Page.Content class="space-y-8">
		<ContactBar contact={person.contact} />
		<Contact contact={person.contact} />
		<PersonOrganisations {person} />
	</Page.Content>
	<Page.Footer><Permissions entity={person} /></Page.Footer>
</Page.Root>
