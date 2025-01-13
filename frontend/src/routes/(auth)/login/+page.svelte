<script lang="ts">
import type { PageData } from "./$types.js";
import LoginForm from "./login-form.svelte";

const { data }: { data: PageData } = $props();
</script>

<header>
	<h1 class="mb-3 text-3xl font-bold">Connexion</h1>
	<p class="text-sm text-foreground/60">
		Entrez votre email et votre mot de passe pour vous connecter
	</p>
</header>

<LoginForm data={data.form} />

<footer>
	<div class="w-full text-center text-sm">
		<p class="mb-3 text-sm text-foreground/60">
			Première connexion ? <a href="/recover-password" class="underline">
				Demandez votre mot de passe
			</a>
		</p>
		Vous n'avez pas encore de compte ?
		<a href="/signup" class="underline">Inscrivez-vous</a>
	</div>
</footer>
