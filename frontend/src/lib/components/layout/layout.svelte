<script lang="ts">
	const { children } = $props();

	import AppSidebar from "$lib/components/layout/sidebar.svelte";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import Header from "./header.svelte";
</script>

<Sidebar.Provider>
	<AppSidebar />
	<Sidebar.Inset>
		<Header />
		{@render children()}
	</Sidebar.Inset>
</Sidebar.Provider>
