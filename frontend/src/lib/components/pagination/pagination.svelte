<script lang="ts">
	import { goto } from '$app/navigation';
	import * as Pagination from '$lib/components/ui/pagination';
	import { ChevronLeft, ChevronRight } from 'lucide-svelte';

	type Props = {
		total: number;
		limit: number;
		offset: number;
		urlPrefix: string;
	};
	const { total, limit, offset, urlPrefix } = $props();
	let pageNumber = $derived(Math.floor(offset / limit) + 1);
</script>

{#if total > limit}
	<Pagination.Root
		count={total}
		perPage={limit}
		page={pageNumber}
		controlledPage
		onPageChange={(p) => {
			goto(`${urlPrefix}?offset=${(p - 1) * limit}&limit=${limit}`);
		}}
	>
		{#snippet children({ pages, currentPage })}
			<Pagination.Content>
				<Pagination.Item>
					<Pagination.PrevButton>
						<ChevronLeft class="size-4" />
						<span>Précédent</span>
					</Pagination.PrevButton>
				</Pagination.Item>
				{#each pages as page (page.key)}
					{#if page.type === 'ellipsis'}
						<Pagination.Item>
							<Pagination.Ellipsis />
						</Pagination.Item>
					{:else}
						<Pagination.Item>
							<Pagination.Link {page} isActive={currentPage === page.value} />
						</Pagination.Item>
					{/if}
				{/each}
				<Pagination.Item>
					<Pagination.NextButton>
						<ChevronRight class="size-4" />
						<span>Suivant</span>
					</Pagination.NextButton>
				</Pagination.Item>
			</Pagination.Content>
		{/snippet}
	</Pagination.Root>
{/if}
