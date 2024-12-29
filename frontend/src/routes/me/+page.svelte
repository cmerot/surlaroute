<script lang="ts">
	import Contact from '$lib/components/directory/contact.svelte';
	import PersonOrganisations from '$lib/components/directory/page/person-organisations.svelte';
	import PersonResult from '$lib/components/directory/result/person-result.svelte';
	import { Account, Person } from '$lib/components/icons2';
	import * as Page from '$lib/components/page';
	import Permission from '$lib/components/permissions/permission.svelte';
	import Permissions from '$lib/components/permissions/permissions.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import * as Card from '$lib/components/ui/card';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import { Edit } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	// const user = data.user;

	const { user, person } = data;

	const description: string[] = $state([]);
	onMount(() => {
		if (!person) {
			return;
		}

		if (person.role) {
			description.push(person.role);
		}
		if (person.contact?.address?.q) {
			description.push(person.contact.address.q);
		}
	});

	const title: string = $state(person?.name || user.email);
</script>

<!-- <Page.Root>
	<Page.Title>Mon compte</Page.Title>
	<Page.Description>
		{user.email}
	</Page.Description>
	<Page.Content>
		{#if user.person}
			<PersonResult person={user.person} />
		{/if}
		<Card.Root>
			<Card.Header>
				<Card.Title></Card.Title>
				<Card.Description></Card.Description>
			</Card.Header>
		</Card.Root>
	</Page.Content>
</Page.Root> -->

<Page.Root>
	<Page.Title Icon={Account}>Mon compte</Page.Title>
	{#if description.length > 0}
		<Page.Description>Détail de vos informations personnelles</Page.Description>
	{/if}
	<Page.Content class="space-y-8">
		<Card.Root>
			<Card.Header>
				<Card.Title>Paramètres de connexion</Card.Title>
				<Card.Description></Card.Description>
			</Card.Header>
			<Card.Content>
				<p><strong>Identifiant: </strong> {user.email}</p>
				<p><strong>Mot de passe: </strong> **********</p>
			</Card.Content>
			<Card.Footer>
				<Button disabled>Changer votre mot de passe</Button>
			</Card.Footer>
		</Card.Root>

		{#if person}
			<Contact contact={person.contact} />
			<PersonOrganisations {person} />
		{:else}
			<Card.Root>
				<Card.Header>
					<Card.Title>Ajouter des informations personnelles</Card.Title>
					<Card.Description>
						Vous n'avez pas d'informations personnelles rattachées à votre compte.
					</Card.Description>
				</Card.Header>
				<Card.Content class="prose dark:prose-invert">
					<div class="mt-4 flex items-center space-x-4">
						<Skeleton class="size-12 rounded-full" />
						<div class="space-y-2">
							<Skeleton class="h-4 w-[250px]" />
							<Skeleton class="h-4 w-[200px]" />
						</div>
					</div>
				</Card.Content>
				<Card.Footer>
					<Button disabled>Enregistrer</Button>
				</Card.Footer>
			</Card.Root>
		{/if}
	</Page.Content>
	{#if person}
		<Page.Footer><Permissions entity={person} /></Page.Footer>
	{/if}
</Page.Root>
