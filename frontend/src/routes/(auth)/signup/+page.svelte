<script lang="ts">
	import type { PageData } from "./$types.js";
	import SignupForm from "./signup-form.svelte";
	export let data: PageData;
</script>

<header>
	<h1 class="mb-3 text-3xl font-bold">Inscription</h1>
	<p class="text-sm text-foreground/60">Entrez vos informations pour vous créer un compte</p>
</header>

<SignupForm data={data.form} />

<footer>
	<div class="w-full text-center text-sm">
		Vous avez déjà un compte ?
		<a href="/login" class="underline">Connexion</a>
	</div>
</footer>
