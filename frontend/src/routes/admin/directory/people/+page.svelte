<script lang="ts">
	import type { PageData } from './$types';
	import * as Table from '$lib/components/ui/table/index.js';
	import type { PersonPublic } from '$lib/backend/client';
	import { Button } from '$lib/components/ui/button';
	import { Plus } from 'lucide-svelte';

	let { data }: { data: PageData } = $props();
	const { results: people = [] as PersonPublic[] } = data;
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
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
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>

<a href="/admin/directory/people/create" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
