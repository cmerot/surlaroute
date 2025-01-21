<script lang="ts">
	import AppSidebar from "$lib/components/layout/sidebar.svelte";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import Header from "./header.svelte";
	const { children } = $props();
</script>

<Sidebar.Provider>
	<AppSidebar />
	<Sidebar.Inset>
		<Header />
		{@render children()}
	</Sidebar.Inset>
</Sidebar.Provider>
