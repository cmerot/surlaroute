<script lang="ts">
	import Pagination from '$lib/components/pagination.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table/index.js';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	let users = $derived(data.results);
	let total = $derived(data.total);
	let limit = $derived(data.limit);
	let offset = $derived(data.offset);
</script>

<!-- <pre>{JSON.stringify(users, null, 2)}</pre> -->
<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Email de connexion</Table.Head>
			<Table.Head>Membre Armodo</Table.Head>
			<Table.Head>Actif</Table.Head>
			<Table.Head>Admin</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each users as user}
			<Table.Row>
				<Table.Cell>
					<a href="/admin/users/{user.id}" class="block hover:underline">
						{#if user.person}
							<p>{user.person.name}</p>
						{/if}
						<span>{user.email}</span>
					</a>
				</Table.Cell>
				<Table.Cell>{user.is_member ? 'Oui' : 'Non'}</Table.Cell>
				<Table.Cell>{user.is_active ? 'Oui' : 'Non'}</Table.Cell>
				<Table.Cell>{user.is_superuser ? 'Oui' : 'Non'}</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>
<Pagination {total} {limit} {offset} urlPrefix="/admin/users" />

<a href="/admin/users/register" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
