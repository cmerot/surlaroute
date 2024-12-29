<script lang="ts">
	import { DisciplineBadge } from '$lib/components/discipline-badge';
	import { Mobility, Tour } from '$lib/components/icons2';
	import * as Page from '$lib/components/page';
	import Pagination from '$lib/components/pagination/pagination.svelte';
	import * as Card from '$lib/components/ui/card';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();

	const { results: tours, total, limit, offset } = data;
</script>

<Page.Root>
	<Page.Title class="flex items-center" Icon={Tour}>
		<span class="grow">Tournées</span>
	</Page.Title>
	<Page.Description>
		<p>Par les membres</p>
	</Page.Description>
	<Page.Content class="space-y-4">
		{#each tours as tour}
			<a href="/tours/{tour.id}" class="block">
				<Card.Root class="hover:bg-accent">
					<Card.Header>
						<Card.Title>
							{tour.name}
						</Card.Title>
						{#if tour.description}
							<Card.Description>{tour}</Card.Description>
						{/if}
					</Card.Header>
					<Card.Content class="flex gap-4">
						{tour.year}
						{#each tour.disciplines as discipline}
							<DisciplineBadge {discipline} />
						{/each}
						{#each tour.mobilities as mobility}
							<Mobility {mobility} />
						{/each}
					</Card.Content>
				</Card.Root>
			</a>
		{/each}
	</Page.Content>
	<Page.Footer>
		<Pagination {total} {limit} {offset} urlPrefix="/admin/directory/tours" />
	</Page.Footer>
</Page.Root>
