<script lang="ts">
	import { type ActorAssocPublic } from '$lib/backend/client/types.gen';
	type Props = { members: ActorAssocPublic[] | null | undefined };
	let { members }: Props = $props();
</script>

{#if members}
	<h2>Membres</h2>

	{#each members as member}
		{#if member.actor.type === 'Person'}
			<p>
				<a href="/admin/directory/people/{member.actor.id}" class="block hover:underline">
					{member.actor.name}
				</a>
			</p>
		{:else}
			<p>
				<a href="/admin/directory/orgs/{member.actor.id}" class="block hover:underline">
					{member.actor.name}
				</a>
			</p>
		{/if}
	{/each}
{/if}
