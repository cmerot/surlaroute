<script lang="ts" module>
	// sample data
	const data = {
		versions: ['0.1.0'],
		navMain: [
			{
				title: 'Utilisateurs',
				url: '/admin/users'
			},
			{
				title: 'Tournées',
				url: '/admin/tours',
				items: [
					{
						title: 'Mes tournées',
						url: '/',
						isActive: true
					},
					{
						title: 'Les tournées ArMoDo',
						url: '/'
					}
				]
			},
			{
				title: 'Annuaire ArMoDo',
				url: '/admin/directory',
				items: [
					{
						title: 'Personnes',
						url: '/admin/directory/people'
					},
					{
						title: 'Structures',
						url: '/admin/directory/orgs',
						isActive: true
					}
				]
			}
		]
	};
</script>

<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { Compass } from 'lucide-svelte';
	import type { ComponentProps } from 'svelte';
	let { ref = $bindable(null), ...restProps }: ComponentProps<typeof Sidebar.Root> = $props();
</script>

<Sidebar.Root bind:ref {...restProps}>
	<Sidebar.Header>
		<Sidebar.Menu>
			<Sidebar.MenuItem>
				<Sidebar.MenuButton size="lg">
					{#snippet child({ props })}
						<a href="/" {...props}>
							<div
								class="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg"
							>
								<Compass class="size-6" />
							</div>
							<div class="flex flex-col gap-0.5 leading-none">
								<span class="font-semibold">Sur la route</span>
							</div>
						</a>
					{/snippet}
				</Sidebar.MenuButton>
			</Sidebar.MenuItem>
		</Sidebar.Menu>
	</Sidebar.Header>
	<Sidebar.Content>
		<Sidebar.Group>
			<Sidebar.Menu>
				{#each data.navMain as groupItem (groupItem.title)}
					<Sidebar.MenuItem>
						<Sidebar.MenuButton>
							{#snippet child({ props })}
								<a href={groupItem.url} class="font-medium" {...props}>
									{groupItem.title}
								</a>
							{/snippet}
						</Sidebar.MenuButton>
						{#if groupItem.items?.length}
							<Sidebar.MenuSub>
								{#each groupItem.items as item (item.title)}
									<Sidebar.MenuSubItem>
										<Sidebar.MenuSubButton isActive={item.isActive}>
											{#snippet child({ props })}
												<a href={item.url} {...props}>{item.title}</a>
											{/snippet}
										</Sidebar.MenuSubButton>
									</Sidebar.MenuSubItem>
								{/each}
							</Sidebar.MenuSub>
						{/if}
					</Sidebar.MenuItem>
				{/each}
			</Sidebar.Menu>
		</Sidebar.Group>
	</Sidebar.Content>
	<Sidebar.Rail />
</Sidebar.Root>
