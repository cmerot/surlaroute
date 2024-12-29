<script lang="ts">
	import { Ban, Check } from 'lucide-svelte';
	import { Button } from '../ui/button';

	interface PermissionProps {
		name: string;
		value?: boolean;
	}

	const { name, value }: PermissionProps = $props();
</script>

{#if value}
	<Button>
		<Check class="inline size-5" />
		{name}
	</Button>
{:else}
	<Button variant="destructive">
		<Ban class="inline size-4" />
		{name}
	</Button>
{/if}
