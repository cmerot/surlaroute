<script>
	import * as Alert from '$lib/components/ui/alert';
	import { CircleAlert } from 'lucide-svelte';

	const { error } = $props();
</script>

{#if error}
	<Alert.Root variant="destructive">
		<CircleAlert class="size-4" />
		<Alert.Title>Erreur</Alert.Title>
		<Alert.Description>{error}</Alert.Description>
	</Alert.Root>
{/if}
