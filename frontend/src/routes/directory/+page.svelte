<script lang="ts">
	import { activitiesReadActivities, type TreePublic } from '$lib/backend/client';
	import OrgResult from '$lib/components/directory/result/org-result.svelte';
	import PersonResult from '$lib/components/directory/result/person-result.svelte';
	import { Directory } from '$lib/components/icons2';
	import * as Page from '$lib/components/page/index.js';
	import Pagination from '$lib/components/pagination/pagination.svelte';
	import SearchForm from '$lib/components/search-form/search-form.svelte';
	import type { ActionData, PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const activities = $derived(data.activitiesResult.results);
	const actors = $derived(data.actorsResult.results);
	const total = $derived(data.actorsResult.total);
	const limit = $derived(data.actorsResult.limit);
	const offset = $derived(data.actorsResult.offset);

	let selectedActivityValue = $state('');
	const selectedActivityName = $derived(
		activities.find((f) => f.path === selectedActivityValue)?.name ?? 'Toutes les catégories'
	);
</script>

<Page.Root>
	<Page.Title class="flex items-center" Icon={Directory}>
		<span class="grow">Annuaire</span>
	</Page.Title>
	<Page.Content class="space-y-8">
		<!-- <SearchForm /> -->

		<!-- <form method="GET" class="flex space-x-4">
			<InputSearch name="q" />
			<Select.Root type="single" name="activity" bind:value={selectedActivityValue}>
				<Select.Trigger class="w-[180px]">{selectedActivityName}</Select.Trigger>
				<Select.Content>
					{#each activities as activity, index}
						<Select.Item value={activity.path}>
							<div class="w-full">
								<div>
									{activity.name}
								</div>
								<div class="text-muted-foreground">
									{activity.path}
								</div>
							</div>
						</Select.Item>
					{/each}
				</Select.Content>
			</Select.Root>
		</form> -->
		<div class="space-y-4">
			{#each actors as actor}
				{#if actor.type == 'Org'}
					<OrgResult org={actor} />
				{:else}
					<PersonResult person={actor} />
				{/if}
			{/each}
		</div>
	</Page.Content>
	<Page.Footer>
		<Pagination {total} {limit} {offset} urlPrefix="/directory" />
	</Page.Footer>
</Page.Root>
