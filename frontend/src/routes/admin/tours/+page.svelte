<script lang="ts">
	import Pagination from '$lib/components/pagination.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();

	let tours = $derived(data.results);
	let total = $derived(data.total);
	let limit = $derived(data.limit);
	let offset = $derived(data.offset);
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
			<Table.Head>Année</Table.Head>
			<Table.Head>Discipline</Table.Head>
			<Table.Head>Mobilité</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each tours as tour}
			<Table.Row>
				<Table.Cell>
					<a href="/admin/tours/{tour.id}" class="block hover:underline">
						{tour.name}
					</a>
				</Table.Cell>
				<Table.Cell>
					{tour.year}
				</Table.Cell>
				<Table.Cell>
					{tour.disciplines?.map((m) => m.name).join(', ')}
				</Table.Cell>
				<Table.Cell>
					{tour.mobilities?.map((m) => m.name).join(', ')}
				</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>
<Pagination {total} {limit} {offset} urlPrefix="/admin/directory/tours" />

<a href="/admin/directory/tours/create" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
