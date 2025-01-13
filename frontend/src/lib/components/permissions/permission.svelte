<script lang="ts">
import { Badge } from "$lib/components/ui/badge";
import { Ban, Check } from "lucide-svelte";
import { Button } from "$lib/components/ui/button";

interface PermissionProps {
	name: string;
	value?: boolean;
}

const { name, value }: PermissionProps = $props();
</script>

{#if value}
	<Badge>
		<Check class="mr-2 inline size-5" />
		{name}
	</Badge>
{:else}
	<Badge variant="destructive">
		<Ban class="mr-2 inline size-5" />
		{name}
	</Badge>
{/if}
