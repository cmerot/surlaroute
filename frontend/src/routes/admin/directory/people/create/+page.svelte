<script lang="ts">
	import { page } from '$app/stores';
	import { addCrumb } from '$lib/utils';
	import type { PageData } from './$types.js';
	import Form from './form.svelte';

	addCrumb($page.url.pathname, 'Nouvel utilisateur');
	export let data: PageData;
</script>

<div class="p-4">
	<Form data={data.form} />
</div>
