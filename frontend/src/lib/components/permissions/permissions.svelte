<script lang="ts">
	import type { OrgPublic, PersonPublic, TourPublic } from '$lib/backend/client';
	import { Button } from '$lib/components/ui/button';
	import { buttonVariants } from '$lib/components/ui/button/index.js';
	import * as Sheet from '$lib/components/ui/sheet/index.js';
	import { ShieldEllipsis } from 'lucide-svelte';
	import Permission from './permission.svelte';

	type PermissionsProps = {
		entity: OrgPublic | PersonPublic | TourPublic;
	};

	const { entity }: PermissionsProps = $props();
</script>

<Sheet.Root>
	<Sheet.Trigger class={buttonVariants({ variant: 'outline' })}>
		<ShieldEllipsis class="size-5" />
	</Sheet.Trigger>
	<Sheet.Content side="right">
		<Sheet.Header>
			<Sheet.Title>Permissions</Sheet.Title>
		</Sheet.Header>
		<div class="mt-4 space-y-4">
			<div>
				<h3 class="mb-4 text-xl">Qui peut lire cette fiche</h3>
				<ul class="space-y-2">
					<li>
						<Permission name="tout le monde" value={entity.other_read} />
					</li>
					<li>
						<Permission
							name="membres du groupe {entity.group_owner?.name}"
							value={entity.group_read}
						/>
					</li>
					<li>
						<Permission name="membres armodo" value={entity.member_read} />
					</li>
				</ul>
			</div>
			{#if entity.owner || entity.group_owner}
				<div class="space-y-2">
					<h3 class="mb-4 text-xl">Propriétaire de la fiche</h3>
					<ul>
						{#if entity.owner?.person}
							<li>
								Utilisateur :
								<Button
									variant="ghost"
									href={`/directory/people/${entity.owner.person.id}`}
									size="sm"
								>
									{entity.owner.person.name}
								</Button>
							</li>
						{/if}

						{#if entity.group_owner}
							<li>
								Groupe :
								<Button variant="ghost" href={`/directory/orgs/${entity.group_owner.id}`} size="sm">
									{entity.group_owner.name}
								</Button>
							</li>
						{/if}
					</ul>
				</div>
			{/if}
		</div>
	</Sheet.Content>
</Sheet.Root>
