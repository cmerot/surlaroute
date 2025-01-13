<script lang="ts" module>
import type { HTMLAnchorAttributes } from "svelte/elements";
export type ActivityBadgeProps = HTMLAnchorAttributes & {
	activity: TreePublic;
};
</script>

<script lang="ts">
	import type { TreePublic } from "$lib/backend/client";
	import Badge from "../ui/badge/badge.svelte";
	let { activity: activity, ...restProps }: ActivityBadgeProps = $props();
</script>

<Badge variant="secondary" {...restProps}>
	{activity.name}
</Badge>
