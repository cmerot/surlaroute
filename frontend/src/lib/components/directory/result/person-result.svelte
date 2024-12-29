<script lang="ts">
	import type { OrgLite_Explore, OrgLiteAssoc_Explore, Person_Explore } from '$lib/backend/client';

	import { Org, Person } from '$lib/components/icons2';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { onMount } from 'svelte';
	import type { SvelteHTMLElements } from 'svelte/elements';
	import ContactDetails from './contact-result.svelte';

	type ActorProps = SvelteHTMLElements['div'] & {
		person: Person_Explore;
	};

	const { person, class: classNames, ...restProps }: ActorProps = $props();

	const href = `/directory/people/${person.id}`;

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

<Card.Root {...restProps}>
	<Card.Header class="min-h-24">
		<Card.Title class="flex font-logo font-normal">
			<span class="grow hover:underline">
				<a {href}>
					{person.name}
				</a>
			</span>
			<Person class="size-5" />
		</Card.Title>

		<Card.Description class="flex items-baseline">
			<span class="grow capitalize">
				{description.join(', ')}
			</span>
			<ContactDetails contact={person.contact} class="text-primary" />
		</Card.Description>
	</Card.Header>
	<Card.Content class="p-2">
		{#each person.membership_assocs as assoc}
			<Button
				href="/directory/orgs/{assoc.org.id}"
				class="flex w-full justify-start"
				variant="ghost"
			>
				<Org class="inline" />
				{assoc.org.name}
				{#if assoc.data?.role}
					({assoc.data.role})
				{/if}
			</Button>
		{/each}
	</Card.Content>
</Card.Root>
