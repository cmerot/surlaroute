<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
</script>

<div class="flex items-center justify-center h-screen">
	<Card.Root class="mx-auto max-w-sm">
		<Card.Header>
			<Card.Title class="text-xl">Inscription</Card.Title>
			<Card.Description>Entrez vos informations pour créer un compte</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4">
				<div class="grid grid-cols-2 gap-4">
					<div class="grid gap-2">
						<Label for="first-name">Prénom</Label>
						<Input id="first-name" placeholder="Max" required />
					</div>
					<div class="grid gap-2">
						<Label for="last-name">Nom</Label>
						<Input id="last-name" placeholder="Robinson" required />
					</div>
				</div>
				<div class="grid gap-2">
					<Label for="email">Email</Label>
					<Input id="email" type="email" placeholder="m@example.com" required />
				</div>
				<div class="grid gap-2">
					<Label for="password">Mot de passe</Label>
					<Input id="password" type="password" />
				</div>
				<Button type="submit" class="w-full">Créer un compte</Button>
			</div>
			<div class="mt-4 text-center text-sm">
				Vous avez déjà un compte ?
				<a href="/login" class="underline">Connexion</a>
			</div>
		</Card.Content>
	</Card.Root>
</div>
