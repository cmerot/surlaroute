<script lang="ts">
	import type { PageData } from './$types';
	import * as Table from '$lib/components/ui/table/index.js';
	import type { UserPublic } from '$lib/backend/client';
	import { Button } from '$lib/components/ui/button';
	import { Plus } from 'lucide-svelte';

	let { data }: { data: PageData } = $props();
	const { data: users = [] as UserPublic[] } = data;
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
			<Table.Head>Email</Table.Head>
			<Table.Head>Actif</Table.Head>
			<Table.Head>Admin</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each users as user}
			<Table.Row>
				<Table.Cell>
					<a href="/admin/users/{user.id}" class="block hover:underline">
						{user.full_name || user.email}
					</a>
				</Table.Cell>
				<Table.Cell>{user.email}</Table.Cell>
				<Table.Cell>{user.is_active ? 'Oui' : 'Non'}</Table.Cell>
				<Table.Cell>{user.is_superuser ? 'Oui' : 'Non'}</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>

<a href="/admin/users/register" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
