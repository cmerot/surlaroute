<script lang="ts">
	import type { UserPublic } from '$lib/backend/client';
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table/index.js';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	const { results: users = [] as UserPublic[] } = data;
	console.log(users);
</script>

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
						{user.email}
					</a>
				</Table.Cell>
				<Table.Cell>{user.is_active ? 'Oui' : 'Non'}</Table.Cell>
				<Table.Cell>{user.is_superuser ? 'Oui' : 'Non'}</Table.Cell>
				<Table.Cell>{user.is_member ? 'Oui' : 'Non'}</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>

<a href="/admin/users/register" class="fixed bottom-4 right-4 rounded-full shadow-lg">
	<Button variant="default" size="icon" class="rounded-full">
		<Plus class="h-6 w-6" />
	</Button>
</a>
