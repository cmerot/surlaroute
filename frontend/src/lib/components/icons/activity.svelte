<script lang="ts" module>
	import { type IconProps } from "lucide-svelte";

	export type ActivityProps = IconProps & {
		activity: TreePublic;
	};
</script>

<script lang="ts">
	import type { TreePublic } from "$lib/backend/client";
	import { DefaultCategory, Diffusion, Production, Ressource } from ".";
	let { activity, ...restProps }: ActivityProps = $props();
	const { path } = $derived(activity);
</script>

{#if path.match(/^Structure\.Diffusion/)}
	<Diffusion {...restProps} />
{:else if path.match(/^Structure\.Production/)}
	<Production {...restProps} />
{:else if path.match(/^Structure\.Ressource/)}
	<Ressource {...restProps} />
{:else}
	<DefaultCategory {...restProps} />
{/if}
