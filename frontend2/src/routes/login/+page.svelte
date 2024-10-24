<script lang="ts">
	import * as Card from '$lib/components/ui/card/';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Alert, AlertDescription } from '$lib/components/ui/alert';
	import { Toaster, toast } from 'svelte-sonner';
	import { Eye, EyeOff } from 'lucide-svelte';

	let email = $state('');
	let password = $state('');
	let showPassword = $state(false);
	let error = $state('');

	function handleLogin() {
		if (!email || !password) {
			console.log(email, password);
			error = 'Veuillez remplir tous les champs.';
			return;
		}
		// Logique de connexion ici
		console.log('Tentative de connexion avec:', { email, password });
		error = '';
		// Simuler une connexion réussie
		setTimeout(() => {
			toast.success('Connexion réussie!');
		}, 1000);
	}
</script>

<div class="flex items-center justify-center h-screen">
	<Card.Root class="mx-automax-w-sm">
		<Card.Header>
			<Card.Title class="text-2xl">Connexion</Card.Title>
			<Card.Description>
				Entrez votre email et votre mot de passe pour vous connecter
			</Card.Description>
		</Card.Header>
		<Card.Content>
			<form>
				<div class="grid gap-4">
					{#if error}
						<div class="grid gap-2">
							<Alert variant="destructive">
								<AlertDescription>{error}</AlertDescription>
							</Alert>
						</div>
					{/if}
					<div class="grid gap-2">
						<Label for="email">Email</Label>
						<Input
							id="email"
							type="email"
							bind:value={email}
							placeholder="m@example.com"
							required
						/>
					</div>
					<div class="grid gap-2">
						<div class="flex items-center">
							<Label for="password">Mot de passe</Label>
							<a href="recover-password" class="ml-auto inline-block text-sm underline">
								Mot de passe oublié ?
							</a>
						</div>
						<Label for="password" class="sr-only">Mot de passe</Label>
						<div class="relative">
							<Input
								id="password"
								name="password"
								type={showPassword ? 'text' : 'password'}
								required
								placeholder="Mot de passe"
								bind:value={password}
							/>
							<button
								type="button"
								class="absolute right-3 top-1/2 -translate-y-1/2"
								onclick={() => (showPassword = !showPassword)}
							>
								{#if showPassword}
									<EyeOff class="h-5 w-5 text-gray-400" />
								{:else}
									<Eye class="h-5 w-5 text-gray-400" />
								{/if}
							</button>
						</div>
					</div>
					<Button type="submit" class="w-full">Connexion</Button>
				</div>
			</form>
			<div class="mt-4 text-center text-sm">
				Vous n'avez pas encore de compte?
				<a href="/signup" class="underline">S'inscrire</a>
			</div>
		</Card.Content>
	</Card.Root>
</div>

<Toaster />
