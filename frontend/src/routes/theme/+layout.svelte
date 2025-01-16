<script lang="ts">
	import { Button } from "$lib/components/ui/button";
	import FormThemeMode from "./form-theme-mode.svelte";

	const { children } = $props();
</script>

<div class="p-4">
	<Button href="/theme">Base</Button>
	<Button href="/theme/demo">Demo</Button>
	<FormThemeMode />
	{@render children()}
</div>
