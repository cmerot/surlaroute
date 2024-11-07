<script lang="ts">
	import { Toaster } from '$lib/components/ui/sonner';
	import { ModeWatcher } from 'mode-watcher';
	import { setContext } from 'svelte';
	import '../app.css';
	import { toast } from 'svelte-sonner';

	let { children, data } = $props();

	let crumbs = $state({
		'/': 'Accueil'
	});
	setContext('crumbs-data', crumbs);

	$effect(() => {
		if (data.notification) {
			toast(data.notification);
		}
	});
</script>

{@render children()}
<Toaster richColors />
<ModeWatcher />
