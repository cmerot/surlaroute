<script lang="ts">
	import type { OrgInfoPublic, PersonDirectoryPublic, TourDetails } from '$lib/backend/client';
	import { Button } from '$lib/components/ui/button';
	import Permission from './permission.svelte';

	type PermissionsProps = {
		entity: OrgInfoPublic | PersonDirectoryPublic | TourDetails;
	};

	const { entity }: PermissionsProps = $props();
</script>

<div class="space-y-4">
	<div class="space-x-3">
		<span>Qui peut lire : </span>
		<Permission name="tout le monde" value={entity.other_read} />
		<Permission name="membres du groupe" value={entity.group_read} />
		<Permission name="membres armodo" value={entity.member_read} />
	</div>
	{#if entity.owner}
		<div class="space-x-3">
			<span>Propriétaire : </span>
			{#if entity.owner?.person}
				<Button variant="ghost" href={`/directory/people/${entity.owner.person.id}`}>
					{entity.owner.person.name}
				</Button>
				{#if entity.group_owner_id}
					<Button variant="ghost" href={`/directory/orgs/${entity.group_owner_id}`}>
						Groupe propriétaire
					</Button>
				{/if}
			{:else}
				<Button variant="ghost" href={`/admin/users/${entity.owner?.id}`}>
					{entity.owner?.person?.name}
				</Button>
			{/if}
		</div>
	{/if}
</div>
