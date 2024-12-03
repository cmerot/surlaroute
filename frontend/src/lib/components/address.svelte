<script lang="ts">
	import { type AddressGeoPublic } from '$lib/backend/client/types.gen';
	type Props = { address: AddressGeoPublic | null | undefined };
	const { address }: Props = $props();
</script>

{#if address}
	<h3>Adresse</h3>
	<p>{address.q}</p>
	<!-- <pre>{JSON.stringify(address, null, 2)}</pre> -->
{/if}
