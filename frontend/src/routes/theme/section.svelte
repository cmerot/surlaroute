<script lang="ts" module>
import { Button } from "$lib/components/ui/button";
import * as Card from "$lib/components/ui/card";
import type { WithChildren } from "bits-ui";
import clsx from "clsx";
import type { HTMLAttributes } from "svelte/elements";
export type ColorSetProps = WithChildren<
	HTMLAttributes<HTMLDivElement> & {
		name: string;
		title?: string;
	}
>;
</script>

<script lang="ts">
	import { ArrowBigUp, Hash } from "lucide-svelte";

	const {
		name,
		class: className,
		title,
		children,
		...restProps
	}: ColorSetProps = $props();
</script>

<div class={clsx("", className)} {...restProps}>
	<div class="relative">
		{#if title}
			<h1 id={name} class="mb-4 mt-8 font-logo text-2xl">
				{title}
				<Button href="#page" variant="ghost"
					><ArrowBigUp class="h-4 w-4" /></Button
				>
				<Button id={name} href={`#${name}`} variant="ghost"><Hash /></Button>
			</h1>
		{/if}
	</div>
	{@render children?.()}
</div>
