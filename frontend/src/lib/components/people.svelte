<script lang="ts">
	import * as Table from '$lib/components/ui/table';
	const { people } = $props();
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
			<Table.Head>Métier</Table.Head>
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
