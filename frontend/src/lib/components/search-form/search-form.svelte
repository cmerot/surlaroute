<script module lang="ts">
</script>

<script lang="ts">
	import {
		directoryGetActors,
		type DirectoryGetActorsData,
		type OrgFull_Explore,
		type PersonFull_Explore
	} from '$lib/backend/client';
	import { Search } from 'lucide-svelte';
	import type { SvelteHTMLElements } from 'svelte/elements';
	import OrgResult from '../directory/result/org-result.svelte';
	import PersonResult from '../directory/result/person-result.svelte';
	import { InputSearch } from '../input-search';
	import { Button } from '../ui/button';
	import { Input } from '../ui/input';
	type Props = SvelteHTMLElements['div'];

	const { ...restProps } = $props();

	let q = $state('');
	let query: DirectoryGetActorsData = $state({
		query: {
			limit: 10,
			offset: 0,
			q: null
		}
	});
	let open: boolean = $state(false);
	let results: Array<PersonFull_Explore | OrgFull_Explore> = $state([]);

	async function onsubmit() {
		const { data, error } = await directoryGetActors({ query: { q, limit: 10 } });
		if (data) {
			console.log();
			results = data.results;
		} else {
			console.log(error);
		}
	}
	$effect(() => {
		// search(q);
	});
</script>

<div {...restProps}>
	<form {onsubmit} class="relative">
		<Input bind:value={q} type="text" />
		<Button type="submit" class="absolute right-0 top-1/2 -translate-y-1/2 rounded-l-none">
			<Search class="h-5 w-5 " />
		</Button>
	</form>
	{#if results.length > 0 || open}
		<div class="mt-8 space-y-4 bg-pink-500">
			{#each results as actor}
				{#if actor.type == 'Org'}
					<OrgResult org={actor} />
				{:else}
					<PersonResult person={actor} />
				{/if}
			{/each}
		</div>
	{/if}
</div>
