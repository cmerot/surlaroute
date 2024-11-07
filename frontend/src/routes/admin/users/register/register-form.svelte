<script lang="ts">
	import { page } from '$app/stores';
	import FormActionError from '$lib/components/form-action-error.svelte';
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { addCrumb } from '$lib/utils';
	import { type Infer, superForm, type SuperValidated } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { formSchema, type FormSchema } from './schema';
	import { InputPassword } from '$lib/components/input-password';

	const { data } = $props<{ data: SuperValidated<Infer<FormSchema>> }>();
	addCrumb($page.url.pathname, 'Ajouter un utilisateur');

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
	<Form.Field {form} name="full_name">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Nom complet</Form.Label>
				<Input {...props} bind:value={$formData.full_name} />
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
				<InputPassword {...props} bind:value={$formData.password} />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Button class="font-bold">Enregistrer</Form.Button>
</form>
