<script lang="ts">
import type { HTMLInputAttributes } from "svelte/elements";
import type { WithElementRef } from "bits-ui";
import Input from "$lib/components/ui/input/input.svelte";
import { Eye, EyeOff } from "lucide-svelte";

// biome-ignore lint/style/useConst: <explanation>
let {
	ref = $bindable(null),
	value = $bindable(),
	class: className,
	...restProps
}: WithElementRef<HTMLInputAttributes> = $props();

// biome-ignore lint/style/useConst: <explanation>
let showPassword = $state(false);
</script>

<div class="relative">
	<Input
		bind:value
		type={showPassword ? "text" : "password"}
		{...restProps}
	/>
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
