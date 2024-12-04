<script lang="ts">
	import { type EventPublic } from '$lib/backend/client/types.gen';
	import * as Table from '$lib/components/ui/table';
	import { formatISODate } from '$lib/utils';
	const { events }: { events: EventPublic[] } = $props();
	events.sort((a, b) => new Date(a.start_dt).getTime() - new Date(b.start_dt).getTime());
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Date</Table.Head>
			<Table.Head>Lieu de diff</Table.Head>
			<Table.Head>Catégorie de lieu</Table.Head>
			<Table.Head>Adresse</Table.Head>
			<Table.Head>Email</Table.Head>
			<Table.Head>Téléphone</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each events as event}
			{#if event.start_dt}
				<Table.Row>
					<Table.Cell>
						{formatISODate(event.start_dt)}
					</Table.Cell>
					<Table.Cell>
						{event.event_venue.name}
					</Table.Cell>
					<Table.Cell>
						{event.event_venue.activities?.map((activity) => activity.name).join(', ')}
					</Table.Cell>
					<Table.Cell>
						{event.event_venue.contact?.address?.q}
					</Table.Cell>
					<Table.Cell>
						{event.event_venue.contact?.phone_number}
					</Table.Cell>
					<Table.Cell>
						{event.event_venue.contact?.email_address}
					</Table.Cell>
				</Table.Row>
			{/if}
		{/each}
	</Table.Body>
</Table.Root>
