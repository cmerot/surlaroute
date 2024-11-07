<script lang="ts">
	import type { PageData } from './$types.js';
	import RecoverPasswordForm from './recover-password-form.svelte';
	export let data: PageData;
</script>

<header>
	<h1 class="mb-3 text-3xl font-bold">Récupération de mot de passe</h1>
	<p class="text-sm text-foreground/60">
		Entrez votre email pour recevoir un lien de récupération de mot de passe
	</p>
</header>

<RecoverPasswordForm data={data.form} />
