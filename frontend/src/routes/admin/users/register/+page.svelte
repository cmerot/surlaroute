<script lang="ts">
	import { page } from '$app/stores';
	import { addCrumb } from '$lib/utils';
	import type { PageData } from './$types.js';
	import RegisterForm from './register-form.svelte';

	addCrumb($page.url.pathname, 'Nouvel utilisateur');
	export let data: PageData;
</script>

<div class="p-4">
	<RegisterForm data={data.form} />
</div>
