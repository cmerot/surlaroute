<script lang="ts" module>
import type { HTMLAnchorAttributes } from "svelte/elements";
export type MobilityBadgeProps = HTMLAnchorAttributes & {
	mobility: TreePublic;
};
</script>

<script lang="ts">
	import type { TreePublic } from "$lib/backend/client";
	import Badge from "../ui/badge/badge.svelte";

	let { mobility, ...restProps }: MobilityBadgeProps = $props();
</script>

<Badge class={`bg-${mobility.path.toLowerCase()}-500`} {...restProps}>
	{mobility.name}
</Badge>
