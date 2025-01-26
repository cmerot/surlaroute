<script lang="ts">
	import * as Icon from "$lib/components/icons/index.js";
	import { buttonVariants } from "$lib/components/ui/button/index.js";
	import { ScrollArea } from "$lib/components/ui/scroll-area";
	import * as Sheet from "$lib/components/ui/sheet";
	import type { Nav } from "$lib/types/nav";
	import { cn } from "$lib/utils.js";
	import { Menu } from "lucide-svelte";
	import SidebarNav from "./sidebar-nav.svelte";

	const { title, navs }: { title: string; navs: Nav[] } = $props();
	let open = $state(false);
</script>

<Sheet.Root bind:open>
	<Sheet.Trigger
		class={cn(
			buttonVariants({
				variant: "ghost",
				class:
					"mr-4 px-0 text-base hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 md:hidden [&_svg]:size-6",
			}),
		)}
	>
		<Menu size="8" />
		<span class="sr-only">Ouvrir le menu</span>
	</Sheet.Trigger>
	<Sheet.Content side="left" class="bg-sidebar p-0 text-sidebar-foreground">
		<a href="/" class=" flex items-center gap-2 p-4 text-primary">
			<Icon.Logo class="size-8" />
			<span class="mt-1 font-logo text-2xl">
				{title}
			</span>
		</a>

		<ScrollArea orientation="both" class="m-0 h-[calc(100vh-8rem)]">
			<SidebarNav {navs} bind:open />
		</ScrollArea>
	</Sheet.Content>
</Sheet.Root>
