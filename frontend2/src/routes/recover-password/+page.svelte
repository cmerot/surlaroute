<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
</script>

<div class="flex items-center justify-center h-screen">
	<Card.Root class="mx-auto max-w-sm">
		<Card.Header>
			<Card.Title class="text-2xl">Récupération de mot de passe</Card.Title>
			<Card.Description>
				Un email de récupération de mot de passe va être envoyé au compte enregistré.
			</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4">
				<div class="grid gap-2">
					<Input id="email" type="email" placeholder="m@example.com" required />
				</div>
				<Button type="submit" class="w-full">Continuer</Button>
			</div>
		</Card.Content>
	</Card.Root>
</div>
