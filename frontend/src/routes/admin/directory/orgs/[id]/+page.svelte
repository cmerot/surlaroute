<script lang="ts">
	import Contact from '$lib/components/contact.svelte';
	import Members from '$lib/components/members.svelte';
	import { type PageData } from './$types';

	const { data: org }: { data: PageData } = $props();
</script>

<h1>{org.name} ({org.activities?.map((a) => a.name).join(', ')})</h1>

<Contact contact={org.contact} />

<p>{org.description}</p>

<Members members={org.member_assocs} />
