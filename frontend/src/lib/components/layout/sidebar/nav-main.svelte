<script lang="ts">
	import type { SvelteComponent } from "svelte";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";

	const {
		items,
	}: {
		items: {
			title: string;
			url: string;
			icon: typeof SvelteComponent;
			isActive?: boolean;
		}[];
	} = $props();
</script>

<Sidebar.Menu>
	{#each items as item (item.title)}
		<Sidebar.MenuItem>
			<Sidebar.MenuButton isActive={item.isActive}>
				{#snippet child({ props })}
					<a href={item.url} {...props}>
						<item.icon />
						<span>{item.title}</span>
					</a>
				{/snippet}
			</Sidebar.MenuButton>
		</Sidebar.MenuItem>
	{/each}
</Sidebar.Menu>
