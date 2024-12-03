<script lang="ts">
	import { page } from '$app/stores';
	import { addCrumb } from '$lib/utils';
	import type { Snippet } from 'svelte';
	import { type PageData } from './$types';

	let { children, data: person }: { children: Snippet; data: PageData } = $props();

	addCrumb(`/admin/directory/people/${person.id}`, person.name);
</script>

qsdf
{@render children()}
