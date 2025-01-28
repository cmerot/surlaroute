<script lang="ts">
	import type { Nav } from "$lib/types/nav.js";
	import SidebarNavItems from "./sidebar-nav-items.svelte";

	let { navs: navs, open = $bindable(false) }: { navs: Nav[]; open?: boolean } = $props();
</script>

<nav class="w-full space-y-6 p-4">
	{#each navs as nav}
		{#if nav.items.length > 0}
			<div>
				{#if nav.title}
					<h4 class="mb-1 rounded-md px-2 py-1 text-sm font-semibold">
						{nav.title}
					</h4>
				{/if}

				<SidebarNavItems items={nav.items} bind:open />
			</div>
		{/if}
	{/each}
</nav>
