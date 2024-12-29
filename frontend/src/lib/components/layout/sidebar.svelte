<script lang="ts">
	import { ChartLine, Map, Palette, type Icon as IconType } from 'lucide-svelte';

	import { page } from '$app/state';
	import { Account, Directory, Home, Logo, Membership, Tour, Users } from '$lib/components/icons2';
	import NavMain from '$lib/components/layout/sidebar/nav-main.svelte';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { myGlobalState } from '$lib/state.svelte';
	import type { ComponentProps } from 'svelte';
	import NavSecondary from './sidebar/nav-secondary.svelte';

	interface NavItem {
		title: string;
		url: string;
		icon: typeof IconType;
		badge?: string;
		isActive?: boolean;
	}

	interface Data {
		navMain: Array<NavItem>;
		navFavorites: Array<NavItem>;
		navAdmin: Array<NavItem>;
		navUser: Array<NavItem>;
	}

	const data = $state<Data>({
		navMain: [
			// {
			// 	title: 'Explorer',
			// 	url: '/explore',
			// 	icon: Map
			// },
			{
				title: 'Accueil',
				url: '/',
				icon: Home
			},
			{
				title: 'Annuaire',
				url: '/directory',
				icon: Directory
			},
			{
				title: 'Tournées',
				url: '/tours',
				icon: Tour
			}
		],
		navFavorites: [
			{
				title: 'Theme',
				url: '/theme',
				icon: Palette
			}
		],
		navAdmin: [
			{
				title: 'Dashboard',
				url: '/admin',
				icon: ChartLine
			},
			{
				title: 'Tournées',
				url: '/admin/tours',
				icon: Tour
			},
			{
				title: 'Utilisateurs',
				url: '/admin/users',
				icon: Users
			},
			{
				title: 'Annuaire',
				url: '/admin/directory',
				icon: Directory
			}
		],
		navUser: []
	});

	const user = $derived(myGlobalState.user);

	$effect(() => {
		Object.keys(data).forEach((k) => {
			data[k as keyof Data].forEach((i) => {
				if (i.url == '/') {
					i.isActive = page.url.pathname == '/';
				} else {
					i.isActive = page.url.pathname.startsWith(i.url);
				}
			});
		});

		if (user) {
			const url_me = '/me';
			if (!data.navUser.find((i) => i.url == url_me)) {
				data.navUser.push({
					title: 'Mon compte',
					url: url_me,
					icon: Account
				});
			}
		}
		if (user?.person?.membership_assocs) {
			user.person.membership_assocs.forEach((assoc) => {
				const url = `/directory/orgs/${assoc.org.id}`;
				if (!data.navUser.find((i) => i.url == url)) {
					data.navUser.push({
						title: assoc.org.name,
						url,
						icon: Membership
					});
				}
			});
		}
	});

	let { ref = $bindable(null), ...restProps }: ComponentProps<typeof Sidebar.Root> = $props();
</script>

<Sidebar.Root bind:ref class="border-r-0" {...restProps}>
	<Sidebar.Header>
		<div class="kjustify-center mb-4 flex items-center gap-2 text-primary">
			<Logo class="size-12" />
			<span class="mt-1 font-logo text-3xl">Sur la route</span>
		</div>

		<!-- <TeamSwitcher teams={data.teams} /> -->
		<NavMain items={data.navMain} />
	</Sidebar.Header>
	<Sidebar.Content>
		{#if data.navUser.length > 0}
			<NavSecondary items={data.navUser} class="md-auto" title="Mes données" />
		{/if}
		<NavSecondary items={data.navFavorites} class="md-auto" title="Favoris" />
		{#if user?.is_superuser}
			<NavSecondary items={data.navAdmin} class="md-auto" title="Admin" />
		{/if}
	</Sidebar.Content>
	<!-- <Sidebar.SidebarFooter>
	</Sidebar.SidebarFooter> -->
	<Sidebar.Rail />
</Sidebar.Root>
