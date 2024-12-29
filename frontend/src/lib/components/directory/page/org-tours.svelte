<script lang="ts">
	import { type OrgFull_Explore } from '$lib/backend/client';

	import { DisciplineBadge } from '$lib/components/discipline-badge';
	import { Mobility } from '$lib/components/icons2';
	import { Button } from '$lib/components/ui/button';
	import clsx from 'clsx';
	import type { SvelteHTMLElements } from 'svelte/elements';
	import * as Card from '../../ui/card';

	type Props = SvelteHTMLElements['div'] & { org: OrgFull_Explore };

	let { org, class: classNames, ...restProps }: Props = $props();

	console.log(org.tour_assocs);
</script>

{#if org.tour_assocs && org.tour_assocs?.length > 0}
	<Card.Root class={clsx('', classNames)} {...restProps}>
		<Card.Header>
			<Card.Title>Tournées</Card.Title>
		</Card.Header>
		<Card.Content class="p-2">
			<ul class="mt-4">
				{#each org.tour_assocs as assoc}
					<li>
						<Button href="/tours/{assoc.tour.id}" class="flex w-full justify-start" variant="ghost">
							{assoc.tour.name}
							{assoc.tour.year}
							{#each assoc.tour.disciplines as discipline}
								<DisciplineBadge {discipline} />
							{/each}
							{#each assoc.tour.mobilities as mobility}
								<Mobility {mobility} />
							{/each}
						</Button>
					</li>
				{/each}
			</ul>
		</Card.Content>
	</Card.Root>
{/if}
