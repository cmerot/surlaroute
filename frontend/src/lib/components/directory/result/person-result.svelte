<script lang="ts">
import type { PersonPublic } from "$lib/backend/client";

import { Org, Person } from "$lib/components/icons";
import { Button } from "$lib/components/ui/button";
import * as Card from "$lib/components/ui/card";
import { onMount } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";
import ContactDetails from "./contact-result.svelte";

type ActorProps = SvelteHTMLElements["div"] & {
	person: PersonPublic;
};

const { person, class: classNames, ...restProps }: ActorProps = $props();

const href = $derived(`/directory/people/${person.id}`);

const description = $derived.by(() => {
	const parts = [];
	if (person.role) {
		parts.push(person.role);
	}
	if (person.contact?.address?.q) {
		parts.push(person.contact.address.q);
	}
	return parts.join(", ");
});
</script>

<Card.Root {...restProps}>
	<Card.Header class="min-h-24">
		<Card.Title class="flex font-normal">
			<span class="grow hover:underline">
				<a {href}>{person.name}</a>
			</span>
			<Person class="size-5" />
		</Card.Title>

		<Card.Description class="flex items-baseline">
			<span class="grow capitalize">
				{description}
			</span>
			<ContactDetails contact={person.contact} class="text-primary" />
		</Card.Description>
	</Card.Header>
	<Card.Footer class="mt-2 flex-wrap gap-2">
		{#each person.membership_assocs as assoc}
			<Button href="/directory/orgs/{assoc.org.id}" variant="outline">
				<Org class="inline" />
				{assoc.org.name}
				{#if assoc.data?.role}
					({assoc.data.role})
				{/if}
			</Button>
		{/each}
	</Card.Footer>
</Card.Root>
