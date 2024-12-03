<script lang="ts">
	import { addCrumb } from '$lib/utils';

	let { children } = $props();
	addCrumb('/admin/directory', 'Annuaire ArMoDo');
</script>

{@render children()}
