<script lang="ts" module>
	import { Logotext } from "$lib/components/icons";
	import type { Icon as IconType } from "lucide-svelte";

	import type { WithoutChildrenOrChild } from "bits-ui";
	import clsx from "clsx";
	import type { HTMLAttributes } from "svelte/elements";
	export type DeclinaisonProps = WithoutChildrenOrChild<
		HTMLAttributes<HTMLDivElement> & {
			name: string;
			Icon: typeof IconType;
		}
	>;
</script>

<script lang="ts">
	const { name, class: className, ...restProps }: DeclinaisonProps = $props();
</script>

<div class={clsx(name, className)} {...restProps}>
	<div class="mb-4 flex">
		<Logotext
			class={`flex-1 border border-dashed outline-${name} text-${name}-500`}
			size="192"
			title={name}
		/>
		<div class="flex flex-1 flex-col">
			<div class={`flex-1 bg-${name}-300 p-4`}>{name}-300</div>
			<div class={`flex-1 bg-${name}-400 p-4`}>{name}-400</div>
			<div class={`flex-1 bg-${name}-500 p-4`}>{name}-500</div>
		</div>
	</div>
</div>
