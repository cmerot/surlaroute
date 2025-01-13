<script lang="ts">
import { goto } from "$app/navigation";
import { DisciplineBadge } from "$lib/components/discipline-badge";
import { Directory, Tour } from "$lib/components/icons";
import Mobility from "$lib/components/icons/mobility.svelte";
import * as Page from "$lib/components/page";
import * as Card from "$lib/components/ui/card";
import * as Pagination from "$lib/components/ui/pagination";
import { ChevronLeft, ChevronRight } from "lucide-svelte";
import type { PageData } from "./$types";

function getPageNumber() {
	return Math.floor(query.offset / query.limit) + 1;
}

function scrollToElement(id: string) {
	const element = document.getElementById(id);
	if (element) {
		element.scrollIntoView({ behavior: "smooth" });
	}
}

async function search() {
	loading = true;
	const searchParams = new URLSearchParams({
		q: query.q,
		limit: query.limit.toString(),
		offset: query.offset.toString(),
	});

	await goto(`?${searchParams.toString()}`, {
		keepFocus: true,
	});
	loading = false;
}

const { data }: { data: PageData } = $props();
const query = $state(data.query);
const pageNumber = $state(getPageNumber());
let loading = $state(false);

$effect(() => {
	if (query.q) {
		query.offset = 0;
	}
});
</script>

<Page.Root>
	<Page.Title class="flex items-center" Icon={Tour}>
		<span class="grow">Tournées</span>
	</Page.Title>
	<Page.Content class="space-y-8">
		{#if data.results.length < 1}
			<p>Pas de résultat</p>
		{:else}
			<div class="space-y-4">
				{#each data.results as tour}
					<a href="/tours/tours/{tour.id}" class="block">
						<Card.Root class="hover:bg-accent">
							<Card.Header>
								<Card.Title>
									{tour.name}
								</Card.Title>
								{#if tour.description}
									<Card.Description>{tour.description}</Card.Description>
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
			</div>
			<Pagination.Root
				count={data.total}
				perPage={query.limit}
				page={pageNumber}
				onPageChange={(p) => {
					query.offset = (p - 1) * query.limit;
					search();
					scrollToElement("search");
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
							{#if page.type === "ellipsis"}
								<Pagination.Item>
									<Pagination.Ellipsis />
								</Pagination.Item>
							{:else}
								<Pagination.Item>
									<Pagination.Link
										{page}
										isActive={currentPage === page.value}
									/>
								</Pagination.Item>
							{/if}
						{/each}
						<Pagination.Item>
							<Pagination.NextButton>
								<span>Suivant</span>
								<ChevronRight class="size-4" />
							</Pagination.NextButton>
						</Pagination.Item>
					</Pagination.Content>
				{/snippet}
			</Pagination.Root>
		{/if}
	</Page.Content>
</Page.Root>
