<script lang="ts">
	import Pagination from '$lib/components/pagination.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();

	let people = $derived(data.results);
	let total = $derived(data.total);
	let limit = $derived(data.limit);
	let offset = $derived(data.offset);
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Contact</Table.Head>
			<Table.Head>Fonction</Table.Head>
			<Table.Head>Email</Table.Head>
			<Table.Head>Téléphone</Table.Head>
			<Table.Head>Stucture(s)</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each people as person}
			<Table.Row>
				<Table.Cell>
					<a href="/admin/directory/people/{person.id}" class="block hover:underline">
						{person.name}
					</a>
				</Table.Cell>
				<Table.Cell>
					{person.role}
				</Table.Cell>
				<Table.Cell>
					{#if person.contact?.email_address}
						<a href="mailto:{person.contact?.email_address}" class="block hover:underline">
							{person.contact?.email_address}
						</a>
					{/if}
				</Table.Cell>
				<Table.Cell>
					{#if person.contact?.phone_number}
						<a href="tel:{person.contact?.phone_number}" class="block hover:underline">
							{person.contact?.phone_number}
						</a>
					{/if}
				</Table.Cell>
				<Table.Cell>
					{#if person.membership_assocs}
						{#each person.membership_assocs as assoc}
							<a href="/admin/directory/orgs/{assoc.org.id}" class="block hover:underline">
								{assoc.org.name}
								{#if assoc.org.contact?.address?.q}
									- {assoc.org.contact?.address?.q}
								{/if}
							</a>
						{/each}
					{/if}
				</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>
<Pagination {total} {limit} {offset} urlPrefix="/admin/directory/people" />

<a href="/admin/directory/people/create" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
