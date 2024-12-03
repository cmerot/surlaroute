<script lang="ts">
	import FormActionError from '$lib/components/form-action-error.svelte';
	import InputPassword from '$lib/components/input-password/input-password.svelte';
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { type Infer, superForm, type SuperValidated } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { formSchema, type FormSchema } from './schema';

	const { data } = $props<{ data: SuperValidated<Infer<FormSchema>> }>();
	let error = $state();
	const form = superForm(data, {
		validators: zodClient(formSchema),
		onError({ result }) {
			error = result.error.message;
		}
	});

	const { form: formData, enhance } = form;
</script>

<form method="POST" use:enhance class="space-y-6">
	<FormActionError {error} />
	<Form.Field {form} name="name">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Nom complet</Form.Label>
				<Input {...props} bind:value={$formData.name} />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="email">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Email</Form.Label>
				<Input {...props} bind:value={$formData.email} />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="password">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Mot de passe</Form.Label>
				<InputPassword {...props} bind:value={$formData.password} type="password" />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Button class="w-full font-bold">Créer un compte</Form.Button>
</form>
