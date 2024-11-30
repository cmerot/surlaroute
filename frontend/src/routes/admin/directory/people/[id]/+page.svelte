<script lang="ts">
	import { page } from '$app/stores';
	import FormActionError from '$lib/components/form-action-error.svelte';
	import * as Accordion from '$lib/components/ui/accordion';
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { addCrumb } from '$lib/utils';
	import { toast } from 'svelte-sonner';
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { type PageData } from './$types';
	import { formSchema } from './schema';

	const { data }: { data: PageData } = $props();
	let error = $state();

	const sform = superForm(data.form, {
		validators: zodClient(formSchema),
		onError({ result }) {
			error = JSON.stringify(result.error);
		}
	});

	const { form, message, enhance } = sform;

	$effect(() => {
		addCrumb($page.url.pathname, $form.name);
	});

	$effect(() => {
		if ($message) {
			toast($message);
		}
	});

	import { buttonVariants } from '$lib/components/ui/button/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import * as Popover from '$lib/components/ui/popover/index.js';
	import Combobox from '$lib/components/combobox/combobox.svelte';
</script>

<div class="p-4">
	<form method="POST" action="?/update" use:enhance class="space-y-6">
		<FormActionError {error} />
		<Form.Field form={sform} name="name">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Nom complet</Form.Label>
					<Input {...props} bind:value={$form.name} />
				{/snippet}
			</Form.Control>
			<Form.FieldErrors />
		</Form.Field>
		<!-- <Form.Field form={sform} name="email">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Email</Form.Label>
					<Input {...props} bind:value={$form.email} />
				{/snippet}
			</Form.Control>
			<Form.FieldErrors />
		</Form.Field> -->
		<Form.Button class="font-bold">Modifier</Form.Button>
	</form>
	<Accordion.Root type="single">
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
</div>
