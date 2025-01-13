<script lang="ts">
import { ActivityBadge } from "$lib/components/activity-badge";
import ContactBar from "$lib/components/directory/contact-bar.svelte";
import Contact from "$lib/components/directory/contact.svelte";
import OrgInformations from "$lib/components/directory/page/org-informations.svelte";
import OrgMembers from "$lib/components/directory/page/org-members.svelte";
import OrgTours from "$lib/components/directory/page/org-tours.svelte";
import { Org } from "$lib/components/icons";
import * as Page from "$lib/components/page";
import Permissions from "$lib/components/permissions/permissions.svelte";
import type { PageData } from "./$types";

const { data }: { data: PageData } = $props();
const org = data.org;
const description: string[] = $state([]);
</script>

<Page.Root>
	<Page.Title Icon={Org}>{org.name}</Page.Title>
	{#if description.length > 0}
		<Page.Description>
			{#each org.activities as activity}
				<ActivityBadge {activity} class="align-middle" />
			{/each}
			<span class="capitalize">
				{description.join(", ")}
			</span>
		</Page.Description>
	{/if}
	<Page.Content class="space-y-8">
		<ContactBar contact={org.contact} />
		<Contact contact={org.contact} />
		<OrgInformations {org} />
		<OrgTours {org} />
		{#if org.member_assocs.length > 0}
			<OrgMembers {org} />
		{/if}
	</Page.Content>
	<Page.Footer><Permissions entity={org} /></Page.Footer>
</Page.Root>
