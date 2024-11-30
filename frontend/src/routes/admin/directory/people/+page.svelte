<script lang="ts">
	import type { PersonPublic } from '$lib/backend/client';
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table/index.js';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	const { results: people = [] as PersonPublic[] } = data;
	console.log(data);
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
			<Table.Head>Métier</Table.Head>
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
					<a href="/admin/directory/people/{person.id}" class="block hover:underline">
						{person.role}
					</a>
				</Table.Cell>
			</Table.Row>
			<Table.Cell>
				<a href="/admin/directory/people/{person.id}" class="block hover:underline">
					<!-- {person.orgs.map((org) => org.name).join(', ')} -->
				</a>
			</Table.Cell>
		{/each}
	</Table.Body>
</Table.Root>

<a href="/admin/directory/people/create" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
