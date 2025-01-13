<script lang="ts">
import { goto } from "$app/navigation";
import OrgResult from "$lib/components/directory/result/org-result.svelte";
import PersonResult from "$lib/components/directory/result/person-result.svelte";
import { Directory } from "$lib/components/icons";
import * as Page from "$lib/components/page";
import { Button } from "$lib/components/ui/button";
import { Input } from "$lib/components/ui/input";
import * as Pagination from "$lib/components/ui/pagination";
import * as Select from "$lib/components/ui/select";
import { ChevronLeft, ChevronRight, Loader, Search, X } from "lucide-svelte";
import type { PageData } from "./$types";

const activityList = [
	{ name: "Toutes les catégories", path: "" },
	{ name: "Diffusion", path: "Structure.Diffusion" },
	{ name: "Ressource", path: "Structure.Ressource" },
	{ name: "Production", path: "Structure.Production" },
];

function getPageNumber() {
	return Math.floor(query.offset / query.limit) + 1;
}

async function search() {
	loading = true;
	const searchParams = new URLSearchParams({
		q: query.q,
		limit: query.limit.toString(),
		offset: query.offset.toString(),
		activity: query.activity,
	});

	await goto(`?${searchParams.toString()}`, {
		keepFocus: true,
	});
	loading = false;
}

function onsubmit(event: Event) {
	event.preventDefault();
	search();
}

function getActivityName(path: string) {
	return (
		activityList.find((f) => f.path === path)?.name ?? "Toutes les catégories"
	);
}

function scrollToElement(id: string) {
	const element = document.getElementById(id);
	if (element) {
		element.scrollIntoView({ behavior: "smooth" });
	}
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
	<Page.Title class="flex items-center" Icon={Directory}>
		<span class="grow">Annuaire</span>
	</Page.Title>
	<Page.Content class="space-y-8">
		<span id="search" class="bg-pink-500"></span>
		<div class="space-y-4">
			<form class="space-y-4" {onsubmit}>
				<input type="hidden" name="offset" value={query.offset} />
				<input type="hidden" name="limit" value={query.limit} />
				<div class="flex gap-4">
					<Select.Root
						type="single"
						name="activity"
						bind:value={query.activity}
						onValueChange={(v) => {
							query.activity = v;
							query.offset = 0;
							search();
						}}
					>
						<Select.Trigger class="w-48"
							>{getActivityName(query.activity)}</Select.Trigger
						>
						<Select.Content class="w-48">
							{#each activityList as activity}
								<Select.Item value={activity.path}>
									{activity.name}
								</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>

					<div class="relative flex-grow">
						<Input
							name="q"
							bind:value={query.q}
							type="text"
							class="rounded-full"
						/>
						<Button
							type="submit"
							class="absolute right-0 top-1/2 -translate-y-1/2 rounded-l-none rounded-r-full"
						>
							<Search class="h-5 w-5" />
						</Button>
						{#if query.q}
							<Button
								type="button"
								class="absolute right-12 top-1/2 -translate-y-1/2 rounded-none"
								variant="ghost"
								onclick={() => {
									query.q = "";
									search();
								}}
							>
								<X class="h-5 w-5" />
								<span class="sr-only">Effacer la recherche</span>
							</Button>
						{/if}
					</div>
				</div>
			</form>

			{#if data.results.length < 1}
				<div class="relative space-y-4">
					<p class="my-4">Pas de résultat</p>
				</div>
			{:else}
				<div class="relative space-y-4">
					{#each data.results as actor}
						{#if actor.type === "Person"}
							<PersonResult person={actor} />
						{:else}
							<OrgResult org={actor} />
						{/if}
					{/each}
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
				</div>
			{/if}
		</div>
	</Page.Content>
</Page.Root>
