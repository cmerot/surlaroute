<script lang="ts">
	import ContactBar from "$lib/components/directory/contact-bar.svelte";
	import Contact from "$lib/components/directory/contact.svelte";
	import PersonOrganisations from "$lib/components/directory/page/person-organisations.svelte";
	import { Person } from "$lib/components/icons";
	import * as Page from "$lib/components/page";
	import Permissions from "$lib/components/permissions/permissions.svelte";
	import type { PageData } from "./$types";

	const { data }: { data: PageData } = $props();
	const person = data.person;
	const description: string[] = $state([]);
</script>

<Page.Root>
	<Page.Title Icon={Person}>{person.name}</Page.Title>
	{#if description.length > 0}
		<Page.Description>
			{description.join(", ")}
		</Page.Description>
	{/if}
	<Page.Content class="space-y-8">
		<ContactBar contact={person.contact} />
		<Contact contact={person.contact} />
		<PersonOrganisations {person} />
	</Page.Content>
	<Page.Footer><Permissions entity={person} /></Page.Footer>
</Page.Root>
