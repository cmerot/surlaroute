<script lang="ts" module>
import type { Icon as IconType } from "lucide-svelte";
export type TitleProps = SvelteHTMLElements["div"] & {
	Icon?: typeof IconType;
};
</script>

<script lang="ts">
	import { cn } from "$lib/utils";
	import type { SvelteHTMLElements } from "svelte/elements";

	let {
		class: className,
		title,
		Icon,
		children,
		...restProps
	}: TitleProps = $props();
</script>

<h1
	class={cn(
		"mt-4 flex px-4  align-middle font-logo text-3xl lg:mt-10 lg:text-5xl",
		className
	)}
	{...restProps}
>
	<div class="grow">{@render children?.()}</div>
	{#if Icon}
		<Icon class="size-7 lg:size-10" />
	{/if}
</h1>
