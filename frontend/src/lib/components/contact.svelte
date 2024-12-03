<script lang="ts">
	import { type ContactPublic } from '$lib/backend/client/types.gen';
	import Address from '$lib/components/address.svelte';
	type Props = { contact: ContactPublic | null | undefined };
	let { contact }: Props = $props();
</script>

{#if contact}
	<h2>Contact</h2>
	<p><a href="mailto:{contact.email_address}">{contact.email_address}</a></p>
	<p><a href="tel:{contact.phone_number}">{contact.phone_number}</a></p>
	<p>{contact.website}</p>
	<!-- <pre>{JSON.stringify({ ...contact, address: undefined }, null, 2)}</pre> -->

	<Address address={contact.address} />
{/if}
