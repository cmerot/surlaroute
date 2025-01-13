<script lang="ts">
import { page } from "$app/state";
import {
	Account,
	Directory,
	Home,
	Logo,
	Membership,
	Tour,
	Users,
} from "$lib/components/icons";
import NavMain from "$lib/components/layout/sidebar/nav-main.svelte";
// biome-ignore lint/style/useImportType: biome bug, Sidebar components are not types
import * as Sidebar from "$lib/components/ui/sidebar";
import { auth } from "$lib/stores/auth";
import {
	ChartLine,
	Map as LucidMap,
	Palette,
	type Icon as IconType,
} from "lucide-svelte";
import type { ComponentProps } from "svelte";
import NavSecondary from "./sidebar/nav-secondary.svelte";

// Types
interface NavItem {
	title: string;
	url: string;
	icon: typeof IconType;
	badge?: string;
	isActive?: boolean;
}

// biome-ignore lint/style/useConst: biome bug, ref cant be const
let {
	ref = $bindable(null),
	...restProps
}: ComponentProps<typeof Sidebar.Root> = $props();

// State
const staticNavData = $state({
	navMain: [
		{ title: "Accueil", url: "/", icon: Home },
		{ title: "Explorer", url: "/explore", icon: LucidMap },
		{
			title: "Annuaire",
			url: "/directory",
			icon: Directory,
		},
		{ title: "Tournées", url: "/tours", icon: Tour },
	],
	navFavorites: [{ title: "Theme", url: "/theme", icon: Palette }],
	navAdmin: [
		{ title: "Dashboard", url: "/admin", icon: ChartLine },
		{ title: "Tournées", url: "/admin/tours", icon: Tour },
		{
			title: "Utilisateurs",
			url: "/admin/users",
			icon: Users,
		},
		{
			title: "Annuaire",
			url: "/admin/directory",
			icon: Directory,
		},
	],
});

let userNavItems = $state<NavItem[]>([]);
const user = $derived($auth.user);

// Effects
$effect(() => {
	// Update active states
	for (const k of Object.keys(staticNavData)) {
		for (const item of staticNavData[k as keyof typeof staticNavData]) {
			const isActive =
				item.url === "/"
					? page.url.pathname === "/"
					: page.url.pathname.startsWith(item.url);

			(item as NavItem).isActive = isActive;
		}
	}
});

$effect(() => {
	const newUserItems: NavItem[] = [];

	if (user) {
		newUserItems.push({
			title: "Mon compte",
			url: "/me",
			icon: Account,
		});

		if (user.person?.membership_assocs) {
			for (const assoc of user.person.membership_assocs) {
				newUserItems.push({
					title: assoc.org.name,
					url: `/directory/orgs/${assoc.org.id}`,
					icon: Membership,
				});
			}
		}
	}

	userNavItems = newUserItems;
});
</script>

<Sidebar.Root bind:ref class="border-r-0" {...restProps}>
	<Sidebar.Header>
		<div class="kjustify-center mb-4 flex items-center gap-2 text-primary">
			<Logo class="size-12" />
			<span class="mt-1 font-logo text-3xl">Sur la route</span>
		</div>
		<NavMain items={staticNavData.navMain} />
	</Sidebar.Header>

	<Sidebar.Content>
		{#if userNavItems.length > 0}
			<NavSecondary items={userNavItems} title="Mes données" />
		{/if}
		<NavSecondary
			items={staticNavData.navFavorites}
			title="Favoris"
		/>
		{#if user?.is_superuser}
			<NavSecondary
				items={staticNavData.navAdmin}
				title="Admin"
			/>
		{/if}
	</Sidebar.Content>
</Sidebar.Root>
