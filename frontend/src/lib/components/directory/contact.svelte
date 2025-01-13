<script lang="ts">
import type { ContactPublic } from "$lib/backend/client";
import * as Card from "$lib/components/ui/card/index.js";
import { MapPinned } from "lucide-svelte";
import type { SvelteHTMLElements } from "svelte/elements";
import { EmailAddress, PhoneNumber, Website } from "../icons";

type ContactProps = SvelteHTMLElements["div"] & {
	contact?: ContactPublic | null;
};

const { contact, class: classNames, ...restProps }: ContactProps = $props();

let showContact = $state(false);
if (contact) {
	if (
		Object.keys(contact).find((k) => contact[k as keyof typeof contact] != null)
	) {
		showContact = true;
	}
}
</script>

<Card.Root {...restProps}>
	<Card.Header>
		<Card.Title>Coordonnées</Card.Title>
	</Card.Header>
	{#if !contact || !showContact}
		<Card.Content>Pas d'information</Card.Content>
	{:else}
		<Card.Content class="mt-4 space-y-4">
			{#if contact.address?.q}
				<p>
					<MapPinned class="mr-1 inline size-5 align-top" />
					{contact.address.q}
				</p>
			{/if}

			{#if contact.phone_number}
				<p>
					<PhoneNumber class="mr-1 inline size-5 align-top" />
					{contact.phone_number}
				</p>
			{/if}

			{#if contact.website}
				<p>
					<Website class="mr-1 inline size-5 align-top" />
					{contact.website}
				</p>
			{/if}

			{#if contact.email_address}
				<p>
					<EmailAddress class="mr-1 inline size-5 align-top" />
					{contact.email_address}
				</p>
			{/if}
		</Card.Content>
	{/if}
</Card.Root>
