<script lang="ts" module>
	import type { HTMLAnchorAttributes } from 'svelte/elements';
	export type DisciplineBadgeProps = HTMLAnchorAttributes & {
		discipline: TreePublic;
	};
</script>

<script lang="ts">
	import type { TreePublic } from '$lib/backend/client';
	import Badge from '../ui/badge/badge.svelte';
	let { discipline: discipline, ...restProps }: DisciplineBadgeProps = $props();
</script>

<Badge {...restProps}>
	{discipline.name}
</Badge>
