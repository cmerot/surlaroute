<script lang="ts">
	import { Button, buttonVariants } from '$lib/components/ui/button/index.js';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import SearchForm from './search-form.svelte';

	let open: boolean = $state(false);
</script>

<Dialog.Root {open}>
	<Dialog.Trigger class={buttonVariants({ variant: 'outline' })}>Edit Profile</Dialog.Trigger>
	<Dialog.Portal>
		<Dialog.Content>
			<Dialog.Header>
				<Dialog.Title>Edit profile</Dialog.Title>
				<Dialog.Description>
					Make changes to your profile here. Click save when you're done.
				</Dialog.Description>
			</Dialog.Header>
			<SearchForm />
			<Dialog.Footer></Dialog.Footer>
		</Dialog.Content>
	</Dialog.Portal>
</Dialog.Root>
