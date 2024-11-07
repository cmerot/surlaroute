<script lang="ts">
	import type { HTMLInputAttributes } from 'svelte/elements';
	import type { WithElementRef } from 'bits-ui';
	import Input from '$lib/components/ui/input/input.svelte';
	import { Eye, EyeOff } from 'lucide-svelte';
	let showPassword = $state(false);

	let { value = $bindable(), ...restProps }: WithElementRef<HTMLInputAttributes> = $props();
	delete restProps.type;
</script>

<div class="relative">
	<Input bind:value type={showPassword ? 'text' : 'password'} {...restProps} />
	<button
		type="button"
		class="absolute right-3 top-1/2 -translate-y-1/2"
		onclick={() => (showPassword = !showPassword)}
	>
		{#if showPassword}
			<EyeOff class="h-5 w-5 " />
		{:else}
			<Eye class="h-5 w-5 " />
		{/if}
	</button>
</div>
