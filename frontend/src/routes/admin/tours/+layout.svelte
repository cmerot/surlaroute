<script lang="ts">
	import { addCrumb } from '$lib/slr-utils';
	import type { Snippet } from 'svelte';

	let { children }: { children: Snippet } = $props();
	addCrumb('/admin/tours', 'Tournées');
</script>

{@render children()}
