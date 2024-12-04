<script lang="ts">
	import { type OrgPublic } from '$lib/backend/client/types.gen';
	import * as Table from '$lib/components/ui/table';
	const { orgs }: { orgs: OrgPublic[] } = $props();
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Nom</Table.Head>
			<Table.Head>Catégorie de lieu</Table.Head>
			<Table.Head>Adresse</Table.Head>
			<Table.Head>Téléphone</Table.Head>
			<Table.Head>Email</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each orgs as org}
			<Table.Row>
				<Table.Cell>
					{org.name}
				</Table.Cell>
				<Table.Cell>
					{org.activities?.map((activity) => activity.name).join(', ')}
				</Table.Cell>
				<Table.Cell>
					{org.contact?.address?.q}
				</Table.Cell>
				<Table.Cell>
					{org.contact?.phone_number}
				</Table.Cell>
				<Table.Cell>
					{org.contact?.email_address}
				</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>
