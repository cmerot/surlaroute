<script lang="ts" module>
	const userMenu = [
		{
			name: 'Profil',
			href: '/admin/me',
			icon: CircleUser
		},
		{
			name: 'Déconnexion',
			href: '/logout',
			icon: LogOut
		}
	];
</script>

<script lang="ts">
	import { buttonVariants } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { addCrumb } from '$lib/utils';
	import { CircleUser, LogOut, Moon, Sun } from 'lucide-svelte';
	import { resetMode, setMode } from 'mode-watcher';
	import { type Snippet } from 'svelte';
	import AppSidebar from './app-sidebar.svelte';
	import Crumbs from './crumbs.svelte';

	let { children }: { children: Snippet } = $props();
	addCrumb('/admin', 'Admin');
</script>

<Sidebar.Provider>
	<AppSidebar />
	<Sidebar.Inset>
		<header class="flex h-16 shrink-0 items-center gap-2 border-b">
			<div class="flex w-full items-center gap-2 px-3">
				<Sidebar.Trigger />
				<Separator orientation="vertical" class="mr-2 h-4" />
				<Crumbs />
				<div class="ml-auto">
					<DropdownMenu.Root>
						<DropdownMenu.Trigger class={buttonVariants({ variant: 'outline', size: 'icon' })}>
							<Sun
								class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
							/>
							<Moon
								class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
							/>
							<span class="sr-only">Toggle theme</span>
						</DropdownMenu.Trigger>
						<DropdownMenu.Content align="end">
							<DropdownMenu.Item onclick={() => setMode('light')}>Light</DropdownMenu.Item>
							<DropdownMenu.Item onclick={() => setMode('dark')}>Dark</DropdownMenu.Item>
							<DropdownMenu.Item onclick={() => resetMode()}>System</DropdownMenu.Item>
						</DropdownMenu.Content>
					</DropdownMenu.Root>
					<DropdownMenu.Root>
						<DropdownMenu.Trigger class={buttonVariants({ variant: 'outline', size: 'icon' })}>
							<CircleUser class="h-5 w-5" />
							<span class="sr-only">Toggle user menu</span>
						</DropdownMenu.Trigger>
						<DropdownMenu.Content align="end">
							<DropdownMenu.Group>
								<DropdownMenu.GroupHeading>Mon compte</DropdownMenu.GroupHeading>
								<DropdownMenu.Separator />
								{#each userMenu as item}
									<DropdownMenu.Item>
										{#snippet child({ props })}
											<a href={item.href} {...props}>
												<item.icon class="mr-2 size-4" />
												{item.name}
											</a>
										{/snippet}
									</DropdownMenu.Item>
								{/each}
							</DropdownMenu.Group>
						</DropdownMenu.Content>
					</DropdownMenu.Root>
				</div>
			</div>
		</header>
		<div class="flex flex-1 flex-col gap-4 p-4">
			<div class="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min">
				{@render children()}
			</div>
		</div>
	</Sidebar.Inset>
</Sidebar.Provider>
