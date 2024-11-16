<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Search } from 'lucide-svelte';
	// import { debounce } from '$lib/utils';

	import { organisationsReadOrganisations } from '$lib/backend/client/services.gen';
	import type { OrganisationsReadOrganisationsData } from '$lib/backend/client/types.gen.ts';

	let searchTerm = $state('');
	let results = $state([]);
	let isLoading = $state(false);

	const fetchResults = async (term: string) => {
		if (term.length < 2) {
			results = [];
			return;
		}
		console.log(term);
		const data: OrganisationsReadOrganisationsData = {
			query: {
				q: term,
				limit: 10
			}
		};
		const response = await organisationsReadOrganisations(data);
		console.log(response.data?.results);

		isLoading = true;
		try {
			const res = await organisationsReadOrganisations(data);
			// if (res.response.ok) {
			// 	results = await response.json();
			// } else {
			// 	console.error('Failed to fetch results');
			// 	results = [];
			// }
		} catch (error) {
			console.error('Error fetching results:', error);
			results = [];
		} finally {
			isLoading = false;
		}

		// isLoading = true;
		// try {
		// 	const response = await organisationsReadOrganisations();
		// 	if (response.ok) {
		// 		results = await response.json();
		// 	} else {
		// 		console.error('Failed to fetch results');
		// 		results = [];
		// 	}
		// } catch (error) {
		// 	console.error('Error fetching results:', error);
		// 	results = [];
		// } finally {
		// 	isLoading = false;
		// }
	};

	$effect(() => {
		fetchResults(searchTerm);
	});

	// function handleSelect(item) {
	// 	searchTerm = item;
	// 	results = [];
	// }
</script>

<div class="relative">
	<div class="flex w-full items-center space-x-2">
		<Input type="search" placeholder="Search..." bind:value={searchTerm} />
		<Button type="submit" size="icon">
			<Search class="h-4 w-4" />
			<span class="sr-only">Search</span>
		</Button>
	</div>

	<!-- {#if results.length > 0 || isLoading}
		<Command class="absolute left-0 top-full z-50 mt-1 w-full">
			<CommandList>
				<CommandEmpty>No results found.</CommandEmpty>
				{#if isLoading}
					<CommandItem>Searching...</CommandItem>
				{:else}
					{#each results as item}
						<CommandItem value={item} onSelect={() => handleSelect(item)}>
							{item}
						</CommandItem>
					{/each}
				{/if}
			</CommandList>
		</Command>
	{/if} -->
</div>
