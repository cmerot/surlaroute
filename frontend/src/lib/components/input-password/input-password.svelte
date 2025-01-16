<script lang="ts">
	import Input from "$lib/components/ui/input/input.svelte";
	import type { WithElementRef } from "bits-ui";
	import { Eye, EyeOff } from "lucide-svelte";
	import type { HTMLInputAttributes } from "svelte/elements";

	let {
		ref = $bindable(null),
		value = $bindable(),
		...restProps
	}: WithElementRef<HTMLInputAttributes> = $props();

	let showPassword = $state(false);
</script>

<div class="relative">
	<Input bind:value type={showPassword ? "text" : "password"} {...restProps} />
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
