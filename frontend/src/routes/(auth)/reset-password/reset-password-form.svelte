<script lang="ts">
	import FormActionError from '$lib/components/form-action-error.svelte';
	import InputPassword from '$lib/components/input-password/input-password.svelte';
	import * as Form from '$lib/components/ui/form';
	import { formSchema, type FormSchema } from './schema';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

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
	<Form.Field {form} name="newPassword">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Nouveau mot de passe</Form.Label>
				<InputPassword {...props} bind:value={$formData.newPassword} />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="confirmPassword">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Confirmer le nouveau mot de passe</Form.Label>
				<InputPassword {...props} bind:value={$formData.confirmPassword} />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Button variant="secondary" class="w-full font-bold">Changer le mot de passe</Form.Button>
</form>
