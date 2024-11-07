<script lang="ts">
	import { page } from '$app/stores';
	import { addCrumb } from '$lib/utils';

	addCrumb($page.url.pathname, 'Personnes');
</script>

<h1>{$page.url.pathname}</h1>
