<script lang="ts" module>
	import * as Card from "$lib/components/ui/card";
	import type { WithoutChildrenOrChild } from "bits-ui";
	import type { HTMLAttributes } from "svelte/elements";
	export type ColorSetProps = WithoutChildrenOrChild<
		HTMLAttributes<HTMLDivElement> & {
			name: string;
		}
	>;
</script>

<script lang="ts">
	const { name, ...restProps }: ColorSetProps = $props();
</script>

<Card.Root {...restProps}>
	<Card.Header class=" p-0">
		<Card.Title class={`rounded-t-lg bg-${name}-500 p-4`}>
			{name}
		</Card.Title>
	</Card.Header>
	<Card.Content class="rounded p-0">
		<div class={`bg-${name}-50 p-4`}>{name}-50</div>
		<div class={`bg-${name}-100 p-4`}>{name}-100</div>
		<div class={`bg-${name}-200 p-4`}>{name}-200</div>
		<div class={`bg-${name}-300 p-4`}>{name}-300</div>
		<div class={`bg-${name}-400 p-4`}>{name}-400</div>
		<div class={`bg-${name}-500 p-4`}>{name}-500</div>
		<div class={`bg-${name}-600 p-4`}>{name}-600</div>
		<div class={`bg-${name}-700 p-4`}>{name}-700</div>
		<div class={`bg-${name}-800 p-4`}>{name}-800</div>
		<div class={`bg-${name}-900 rounded-b-lg p-4`}>{name}-900</div>
	</Card.Content>
</Card.Root>
