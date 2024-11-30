<script lang="ts">
	import { page } from '$app/stores';
	import FormActionError from '$lib/components/form-action-error.svelte';
	import * as Accordion from '$lib/components/ui/accordion';
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import Switch from '$lib/components/ui/switch/switch.svelte';
	import { addCrumb } from '$lib/utils';
	import { type Infer, superForm, type SuperValidated } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { formSchema, type FormSchema } from './schema';

	const { data } = $props<{ data: SuperValidated<Infer<FormSchema>> }>();
	addCrumb($page.url.pathname, data.data.full_name);
	let error = $state();
	const form = superForm(data, {
		validators: zodClient(formSchema),
		onError({ result }) {
			error = result.error.message;
		}
	});

	const { form: formData, enhance } = form;
</script>

<form method="POST" action="?/update" use:enhance class="space-y-6">
	<FormActionError {error} />
	<Form.Field {form} name="email">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Email</Form.Label>
				<Input {...props} bind:value={$formData.email} />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="is_superuser">
		<Form.Control>
			{#snippet children({ props })}
				<div class="flex items-center space-x-2">
					<Switch {...props} bind:checked={$formData.is_superuser} />
					<Form.Label>Admin</Form.Label>
				</div>
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="is_member">
		<Form.Control>
			{#snippet children({ props })}
				<div class="flex items-center space-x-2">
					<Switch {...props} bind:checked={$formData.is_member} />
					<Form.Label>Membre</Form.Label>
				</div>
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="is_active">
		<Form.Control>
			{#snippet children({ props })}
				<div class="flex items-center space-x-2">
					<Switch {...props} bind:checked={$formData.is_active} />
					<Form.Label>Actif</Form.Label>
				</div>
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Button class="font-bold">Modifier</Form.Button>
</form>
<Accordion.Root type="single" class="w-dfull sm:dmax-w-[70%]">
	<Accordion.Item value="item-1">
		<Accordion.Trigger class="text-destructive ">Supprimer l'utilisateur ?</Accordion.Trigger>
		<Accordion.Content>
			<form method="POST" action="?/delete" use:enhance class="space-y-6">
				<Form.Button formaction="?/delete" variant="destructive" class="font-bold">
					Supprimer
				</Form.Button>
			</form>
		</Accordion.Content>
	</Accordion.Item>
</Accordion.Root>
