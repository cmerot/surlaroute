<script lang="ts">
	import type { PageData } from './$types.js';
	import ResetPassword from './reset-password-form.svelte';
	export let data: PageData;
</script>

<header>
	<h1 class="mb-3 text-3xl font-bold">Réinitialisation du mot de passe</h1>
	<p class="text-sm text-foreground/60">Mettez à jour votre mot de passe ici</p>
</header>

<ResetPassword data={data.form} />
