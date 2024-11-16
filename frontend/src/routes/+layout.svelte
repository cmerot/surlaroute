<script lang="ts">
	import { client } from '$lib/backend/client';
	import { Toaster } from '$lib/components/ui/sonner';
	import { ModeWatcher } from 'mode-watcher';
	import { setContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import '../app.css';

	const VITE_API_URL = import.meta.env.VITE_API_URL;

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
	client.setConfig({
		baseUrl: VITE_API_URL
	});
</script>

{@render children()}
<Toaster richColors />
<ModeWatcher />
