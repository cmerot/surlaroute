<script lang="ts">
	import type { PageData } from './$types';
	import * as Table from '$lib/components/ui/table/index.js';
	import type { OrganisationPublic } from '$lib/backend/client';
	import { Button } from '$lib/components/ui/button';
	import { Plus } from 'lucide-svelte';

	let { data }: { data: PageData } = $props();
	const { results: organisations = [] as OrganisationPublic[] } = data;
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each organisations as organisation}
			<Table.Row>
				<Table.Cell>
					<a href="/admin/directory/organisations/{organisation.id}" class="block hover:underline">
						{organisation.name}
					</a>
				</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>

<a
	href="/admin/directory/organisations/create"
	class="fixed bottom-4 right-4 rounded-full shadow-lg"
>
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
