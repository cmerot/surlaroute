<script lang="ts">
	import { addCrumb } from '$lib/utils';
	import type { Snippet } from 'svelte';

	let { children }: { children: Snippet } = $props();
	addCrumb('/admin/users', 'Utilisateurs');
</script>

{@render children()}
