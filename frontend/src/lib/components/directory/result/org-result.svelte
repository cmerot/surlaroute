<script lang="ts">
	import type { Org_Explore } from '$lib/backend/client';

	import { ActivityBadge } from '$lib/components/activity-badge';
	import { Org, Person } from '$lib/components/icons2';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import clsx from 'clsx';
	import { onMount } from 'svelte';
	import type { SvelteHTMLElements } from 'svelte/elements';
	import ContactDetails from './contact-result.svelte';

	type ActorProps = SvelteHTMLElements['div'] & {
		org: Org_Explore;
	};

	const { org, class: classNames, ...restProps }: ActorProps = $props();

	const href = `/directory/orgs/${org.id}`;

	const description: string[] = $state([]);
	onMount(() => {
		if (org.contact?.address?.q) {
			description.push(org.contact.address.q);
		}
	});
</script>

<Card.Root class={clsx('min-h-24', classNames)} {...restProps}>
	<Card.Header>
		<Card.Title class="flex font-logo font-normal">
			<span class="grow hover:underline">
				<a {href}>
					{org.name}
				</a>
			</span>
			<Org class="size-5" />
		</Card.Title>

		<Card.Description class="flex items-baseline">
			<span class="grow">
				{#each org.activities as activity}
					<ActivityBadge {activity} />
				{/each}
				<span class="capitalize">
					{description.join(', ')}
				</span>
			</span>
			<ContactDetails contact={org.contact} class="text-primary" />
		</Card.Description>
	</Card.Header>

	{#if org.description}
		<Card.Content class="prose dark:prose-invert">
			{org.description}
		</Card.Content>
	{/if}

	{#if org.member_assocs.length > 0}
		<Card.Footer class="p-2">
			{#each org.member_assocs as assoc}
				<Button
					href="/directory/{assoc.actor.type == 'Org' ? 'orgs' : 'people'}/{assoc.actor.id}"
					class="flex w-full justify-start"
					variant="ghost"
				>
					{#if assoc.actor.type == 'Org'}
						<Org class="inline" />
					{:else}
						<Person class="inline" />
					{/if}
					{assoc.actor.name}
					{#if assoc.data?.role}
						({assoc.data.role})
					{/if}
				</Button>
			{/each}
		</Card.Footer>
	{/if}
</Card.Root>
