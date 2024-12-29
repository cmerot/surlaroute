<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import FormThemeMode from './form-theme-mode.svelte';

	let { children } = $props();
</script>

<div class="p-4">
	<Button href="/theme">Base</Button>
	<Button href="/theme/demo">Demo</Button>
	<Button href="/theme/autocomplete">Autocomplete</Button>
	<FormThemeMode />
	{@render children()}
</div>
