<script lang="ts">
	import Input from '$lib/components/ui/input/input.svelte';
	import type { WithElementRef } from 'bits-ui';
	import { Search } from 'lucide-svelte';
	import type { HTMLInputAttributes } from 'svelte/elements';
	import { Button } from '$lib/components/ui/button';

	let { value = $bindable(), ...restProps }: WithElementRef<HTMLInputAttributes> = $props();
</script>

<div class="relative">
	<Input bind:value type="text" {...restProps} />
	<Button type="submit" class="absolute right-0 top-1/2 -translate-y-1/2 rounded-l-none">
		<Search class="h-5 w-5 " />
	</Button>
</div>
