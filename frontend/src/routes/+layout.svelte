<script lang="ts">
	import Layout from '$lib/components/layout/layout.svelte';
	import { setContext } from 'svelte';
	import '../app.css';
	import { myGlobalState } from '../lib/state.svelte';
	let { children, data } = $props();
	$effect(() => {
		myGlobalState.user = data.user;
	});
</script>

<Layout>
	<div class="flex flex-1 flex-col">
		<div class="h-full w-full bg-white/50 dark:bg-black/50">
			{@render children()}
		</div>
	</div>
</Layout>
