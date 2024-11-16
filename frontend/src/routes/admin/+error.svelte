<script lang="ts">
	import { page } from '$app/stores';
</script>

<div class="h-full bg-destructive p-4 text-destructive-foreground">
	<h1 class="mb-10 text-4xl">Oups!</h1>
	<p>Statut de l'erreur: {$page.status}</p>
	<p>{$page.error?.message}</p>
</div>
