<script lang="ts">
	import * as Sidebar from "$lib/components/ui/sidebar";
	import type { ComponentProps } from "svelte";

	let {
		ref = $bindable(null),
		title,
		items,
		...restProps
	}: ComponentProps<typeof Sidebar.Group> & {
		items: {
			title: string;
			url: string;
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			icon: any;
			badge?: string;
			isActive?: boolean;
		}[];
	} = $props();
</script>

<Sidebar.Group bind:ref {...restProps}>
	<Sidebar.GroupLabel>{title}</Sidebar.GroupLabel>
	<Sidebar.GroupContent>
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
					{#if item.badge}
						<Sidebar.MenuBadge>{item.badge}</Sidebar.MenuBadge>
					{/if}
				</Sidebar.MenuItem>
			{/each}
		</Sidebar.Menu>
	</Sidebar.GroupContent>
</Sidebar.Group>
