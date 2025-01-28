<script lang="ts">
	import MobileNav from "$lib/components/site/nav/mobile-nav.svelte";
	import type { Nav } from "$lib/types/nav";
	import { Logo } from "../icons";
	import UserNav from "./nav/user-nav.svelte";

	const { title, navs: navs }: { title: string; navs: Nav[] } = $props();
</script>

<header
	class="sticky top-0 z-[40] w-full bg-sidebar text-sidebar-foreground shadow backdrop-blur supports-[backdrop-filter]:bg-sidebar"
>
	<div class="flex h-16 items-center p-4">
		<MobileNav {title} {navs} />

		<a href="/" class="flex items-center gap-2 text-primary">
			<Logo class="size-8" />
			<span class="mt-1 font-logo text-2xl">
				{title}
			</span>
		</a>

		<UserNav />
	</div>
</header>
