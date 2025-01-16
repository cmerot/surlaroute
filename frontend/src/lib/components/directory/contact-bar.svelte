<script lang="ts">
	import type { ContactPublic } from "$lib/backend/client";
	import clsx from "clsx";
	import { MapPinned } from "lucide-svelte";
	import type { SvelteHTMLElements } from "svelte/elements";
	import { EmailAddress, PhoneNumber, Website } from "../icons";
	import { Button } from "../ui/button";

	type ContactBarProps = SvelteHTMLElements["span"] & {
		contact?: ContactPublic | null;
	};
	const { contact, class: classNames, ...restProps }: ContactBarProps = $props();
</script>

<span class={clsx("flex gap-2", classNames)} {...restProps}>
	{#if contact?.address?.q}
		<Button
			class="flex-1"
			size="lg"
			target="_blank"
			href="https://www.google.com/maps?q={contact.address?.q}"
		>
			<MapPinned />
		</Button>
	{:else}
		<Button disabled={true} class="flex-1" size="lg">
			<MapPinned size="12" />
		</Button>
	{/if}

	{#if contact?.phone_number}
		<Button class="flex-1" size="lg" href="tel:{contact.phone_number}">
			<PhoneNumber />
		</Button>
	{:else}
		<Button disabled={true} class="flex-1" size="lg">
			<PhoneNumber />
		</Button>
	{/if}

	{#if contact?.email_address}
		<Button class="flex-1" size="lg" href="mailto:{contact.email_address}">
			<EmailAddress />
		</Button>
	{:else}
		<Button disabled={true} class="flex-1" size="lg">
			<EmailAddress />
		</Button>
	{/if}

	{#if contact?.website}
		<Button class="flex-1" size="lg" href="mailto:{contact.website}">
			<EmailAddress />
		</Button>
	{:else}
		<Button disabled={true} class="flex-1" size="lg">
			<Website />
		</Button>
	{/if}
</span>
