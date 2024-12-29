<script lang="ts">
	let { children } = $props();

	import AppSidebar from '$lib/components/layout/sidebar.svelte';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { ModeWatcher, resetMode, setMode, setTheme } from 'mode-watcher';
	import Header from './header.svelte';
</script>

<Sidebar.Provider>
	<AppSidebar />
	<Sidebar.Inset>
		<Header />
		{@render children()}
	</Sidebar.Inset>
</Sidebar.Provider>
