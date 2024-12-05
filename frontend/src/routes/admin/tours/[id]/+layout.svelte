<script lang="ts">
	import { page } from '$app/stores';
	import { addCrumb } from '$lib/utils';
	import type { Snippet } from 'svelte';
	import { type PageData } from './$types';

	let { children, data: tour }: { children: Snippet; data: PageData } = $props();

	addCrumb(`/admin/tours/${tour.id}`, tour.name);
</script>

{@render children()}
