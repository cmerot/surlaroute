<script lang="ts" module>
import type { IconProps } from "lucide-svelte";

export type MobilityProps = IconProps & {
	mobility: TreePublic;
};
</script>

<script lang="ts">
	import type { TreePublic } from "$lib/backend/client";
	import { Bateau, Equestre, Marche, Velo } from ".";
	let { mobility, ...restProps }: MobilityProps = $props();
	const { path } = mobility;
</script>

{#if path == "Bateau"}
	<Bateau {...restProps} />
{:else if path == "Equestre"}
	<Equestre {...restProps} />
{:else if path == "Marche"}
	<Marche {...restProps} />
{:else if path == "Velo"}
	<Velo {...restProps} />
{/if}
