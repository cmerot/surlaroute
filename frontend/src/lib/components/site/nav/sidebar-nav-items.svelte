<script lang="ts">
	import type { NavItem as NavItemType } from "$lib/types/nav.js";
	import { cn } from "$lib/utils.js";

	let { items, open = $bindable(false) }: { items: NavItemType[]; open: boolean } = $props();
	function onclick() {
		open = false;
	}
</script>

{#if items.length}
	<div class="grid grid-flow-row auto-rows-max gap-1 text-sm">
		{#each items as { href, disabled = false, external = false, title, active = false, icon: Icon }, index (index)}
			<a
				{onclick}
				{href}
				class={cn(
					"flex h-8 w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left text-sm outline-none hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium data-[active=true]:text-sidebar-accent-foreground [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0",
					disabled && "cursor-not-allowed opacity-60",
				)}
				data-active={active}
				target={external ? "_blank" : ""}
				rel={external ? "noreferrer" : ""}
			>
				<Icon />
				{title}
			</a>
		{/each}
	</div>
{/if}
