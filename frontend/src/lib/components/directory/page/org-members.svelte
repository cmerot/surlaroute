<script lang="ts">
	import { type Org_Explore } from '$lib/backend/client';
	import { Button } from '../../ui/button';

	import clsx from 'clsx';
	import type { SvelteHTMLElements } from 'svelte/elements';
	import { Org, Person } from '../../icons2';
	import * as Card from '../../ui/card';

	type Props = SvelteHTMLElements['div'] & { org: Org_Explore };

	let { org, class: classNames, ...restProps }: Props = $props();
</script>

<Card.Root class={clsx('', classNames)} {...restProps}>
	<Card.Header>
		<Card.Title>Membres</Card.Title>
	</Card.Header>
	<Card.Content class="p-2">
		<ul class="mt-4">
			{#each org.member_assocs as assoc}
				<li>
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
				</li>
			{/each}
		</ul>
	</Card.Content>
</Card.Root>
