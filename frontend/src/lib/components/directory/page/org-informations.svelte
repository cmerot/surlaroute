<script lang="ts">
	import type { OrgPublic } from '$lib/backend/client';

	import clsx from 'clsx';
	import type { SvelteHTMLElements } from 'svelte/elements';
	import * as Card from '../../ui/card';

	type Props = SvelteHTMLElements['div'] & { org: OrgPublic };

	const { org, class: classNames, ...restProps }: Props = $props();
</script>

<Card.Root class={clsx('', classNames)} {...restProps}>
	<Card.Header>
		<Card.Title>Informations</Card.Title>
	</Card.Header>
	<Card.Content class="prose dark:prose-invert">
		<p>{org.description}</p>
		<p>
			<strong>Activité :</strong>
			{org.activities.map((a) => a.name).join(', ')}
		</p>
	</Card.Content>
</Card.Root>
