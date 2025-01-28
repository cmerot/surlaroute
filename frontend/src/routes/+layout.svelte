<script lang="ts">
	import { dev } from "$app/environment";
	import { navigating, page } from "$app/state";
	import { Membership } from "$lib/components/icons";
	import Loading from "$lib/components/loading.svelte";
	import Metadata from "$lib/components/metadata.svelte";
	import SidebarNav from "$lib/components/site/nav/sidebar-nav.svelte";
	import SiteHeader from "$lib/components/site/site-header.svelte";
	import TailwindIndicator from "$lib/components/tailwind-indicator.svelte";
	import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
	import { Toaster } from "$lib/components/ui/sonner";
	import * as Tooltip from "$lib/components/ui/tooltip";
	import { navConfig } from "$lib/config/nav";
	import { siteConfig } from "$lib/config/site";
	import { auth } from "$lib/stores/auth";
	import type { Nav } from "$lib/types/nav";
	import { ModeWatcher } from "mode-watcher";
	import type { Snippet } from "svelte";
	import "../app.css";
	import type { LayoutData } from "./$types";

	type Props = { children: Snippet; data: LayoutData };

	const { children, data }: Props = $props();

	let loading = $derived(!!(navigating?.from && navigating?.to));

	$effect(() => {
		if (data.user && data.authToken) {
			auth.login(data.user, data.authToken);
		} else {
			auth.logout();
		}
	});
	let navs: Nav[] = $state([navConfig.mainNav]);
	$effect(() => {
		const newNavs: Nav[] = [navConfig.mainNav];
		if (data.user) {
			if (data.user.person?.membership_assocs) {
				for (const assoc of data.user.person.membership_assocs) {
					navConfig.userNav.items.push({
						title: assoc.org.name,
						href: `/directory/orgs/${assoc.org.id}`,
						icon: Membership,
					});
				}
			}
			newNavs.push(navConfig.userNav);
			if (data.user?.is_superuser) {
				newNavs.push(navConfig.adminNav);
			}
		}
		navs = newNavs;
	});

	$effect(() => {
		navs.forEach((nav) => {
			nav.items.forEach((item) => {
				if (!item.href) {
					return;
				}
				item.active =
					item.href === "/" ? page.url.pathname === "/" : page.url.pathname.startsWith(item.href);
			});
		});
	});
</script>

<Loading {loading} />
<ModeWatcher />
<Metadata />
<Toaster />
<Tooltip.Provider>
	<div class="flex min-h-screen flex-col">
		<SiteHeader title={siteConfig.name} {navs} />
		<div class="relative grid flex-1 items-start md:grid-cols-[220px_minmax(0,1fr)]">
			<aside class="relative z-[500] hidden h-[calc(100dvh-4rem)] shadow md:sticky md:block">
				<ScrollArea class="h-full space-y-4 bg-sidebar text-sidebar-foreground">
					<SidebarNav {navs} />
				</ScrollArea>
			</aside>
			<div class="flex min-h-[calc(100dvh-4rem)] flex-col">
				{@render children?.()}
			</div>
		</div>
	</div>
</Tooltip.Provider>
{#if dev}
	<TailwindIndicator />
{/if}
