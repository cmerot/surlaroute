<script lang="ts">
	import Pagination from '$lib/components/pagination.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table/index.js';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let orgs = $derived(data.results);
	let total = $derived(data.total);
	let limit = $derived(data.limit);
	let offset = $derived(data.offset);
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
			<Table.Head>Catégorie</Table.Head>
			<Table.Head>Email</Table.Head>
			<Table.Head>Téléphone</Table.Head>
			<Table.Head>Adresse</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each orgs as org}
			<Table.Row>
				<Table.Cell>
					<a href="/admin/directory/orgs/{org.id}" class="block hover:underline">
						{org.name}
					</a>
				</Table.Cell>
				<Table.Cell>
					{org.activities?.map((a) => a.name).join(', ')}
				</Table.Cell>
				<Table.Cell>
					{#if org.contact?.email_address}
						<a href="mailto:{org.contact?.email_address}" class="block hover:underline">
							{org.contact?.email_address}
						</a>
					{/if}
				</Table.Cell>
				<Table.Cell>
					{#if org.contact?.phone_number}
						<a href="tel:{org.contact?.phone_number}" class="block hover:underline">
							{org.contact?.phone_number}
						</a>
					{/if}
				</Table.Cell>
				<Table.Cell>
					{#if org.contact?.address}
						{org.contact?.address.q}
					{/if}
				</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>
<Pagination {total} {limit} {offset} urlPrefix="/admin/directory/orgs" />

<a href="/admin/directory/orgs/create" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
