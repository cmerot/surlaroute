<script lang="ts">
	import Contact from '$lib/components/contact.svelte';
	import { type PageData } from './$types';

	const { data: person }: { data: PageData } = $props();
</script>

<h1>{person.name}</h1>

<Contact contact={person.contact} />
