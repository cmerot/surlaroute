<script lang="ts">
	import NavActions from '$lib/components/layout/header/nav-actions.svelte';
	import { Separator } from '$lib/components/ui/separator';
	import * as Sidebar from '$lib/components/ui/sidebar';
	import SearchFormDialog from '../search-form/search-form-dialog.svelte';
	import Breadcrumb from './breadcrumb.svelte';
</script>

<header class="flex h-14 shrink-0 items-center gap-2">
	<div class="flex flex-1 items-center gap-2 px-3">
		<Sidebar.Trigger />
		<Separator orientation="vertical" class="mr-2 h-4" />
		<Breadcrumb />
		<!-- <SearchFormDialog /> -->
	</div>
	<div class="ml-auto px-3">
		<NavActions />
	</div>
</header>
