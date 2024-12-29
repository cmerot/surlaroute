<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { useSidebar } from '$lib/components/ui/sidebar/index.js';
	import NavMain from './nav-main.svelte';
	let { favorites: items, title } = $props();

	const sidebar = useSidebar();
</script>

<Sidebar.Group class="group-data-[collapsible=icon]:hidden">
	<Sidebar.GroupLabel>{title}</Sidebar.GroupLabel>
	<NavMain {items} />
</Sidebar.Group>
