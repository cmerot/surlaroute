<script lang="ts">
	import { Button } from "$lib/components/ui/button";
	import Input from "$lib/components/ui/input/input.svelte";
	import clsx from "clsx";
	import { Loader, Search, X } from "lucide-svelte";
	import type { SvelteHTMLElements } from "svelte/elements";

	type Props = SvelteHTMLElements["input"] & {
		value?: string;
		loading?: boolean;
	};

	let { value = $bindable(), class: classNames, loading = false, ...restProps }: Props = $props();
</script>

<div class="relative rounded-full shadow-md">
	<Input bind:value type="text" class={clsx("rounded-full", classNames)} {...restProps} />
	<Button
		type="submit"
		class="absolute right-0 top-1/2 -translate-y-1/2 rounded-l-none rounded-r-full"
		disabled={loading}
	>
		{#if loading}
			<Loader class="h-5 w-5 animate-spin" />
		{:else}
			<Search class="h-5 w-5 " />
		{/if}
	</Button>
	{#if value}
		<Button
			class="absolute right-12 top-1/2 -translate-y-1/2 rounded-none"
			variant="ghost"
			onclick={() => (value = "")}
		>
			<X class="h-5 w-5" />
			<span class="sr-only">Effacer la recherche</span>
		</Button>
	{/if}
</div>
