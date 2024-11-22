<script lang="ts">
	import type { OrgPublic } from '$lib/backend/client';
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table/index.js';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	const { results: orgs = [] as OrgPublic[] } = data;
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
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
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>

<a href="/admin/directory/orgs/create" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
