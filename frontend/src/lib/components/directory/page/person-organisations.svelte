<script lang="ts">
	import type { PersonPublic } from "$lib/backend/client";

	import { Org } from "$lib/components/icons";
	import { Button } from "$lib/components/ui/button";
	import clsx from "clsx";
	import type { SvelteHTMLElements } from "svelte/elements";
	import * as Card from "../../ui/card";

	type Props = SvelteHTMLElements["div"] & {
		person: PersonPublic;
	};

	const { person, class: classNames, ...restProps }: Props = $props();
</script>

<Card.Root class={clsx("", classNames)} {...restProps}>
	<Card.Header>
		<Card.Title>Organisations</Card.Title>
	</Card.Header>
	<Card.Content class="p-2">
		<ul class="mt-4">
			{#each person.membership_assocs as assoc}
				<li>
					<Button
						href="/directory/orgs/{assoc.org.id}"
						class="flex w-full justify-start"
						variant="ghost"
					>
						<Org class="inline" />
						{assoc.org.name}
						({assoc.data?.role})
					</Button>
				</li>
			{/each}
		</ul>
	</Card.Content>
</Card.Root>
