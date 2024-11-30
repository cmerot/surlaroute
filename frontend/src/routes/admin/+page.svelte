<script lang="ts">
	import { activitiesReadActivities, orgsReadOrgs, peopleReadPeople } from '$lib/backend/client';
	import type { OrgPublic, TreePublic } from '$lib/backend/client/types.gen.ts';
	import Autocomplete from '$lib/components/autocomplete.svelte';

	let org = $state<OrgPublic>();
	let activity = $state<TreePublic>();
	function renderOrg(org: OrgPublic) {
		return org.name;
	}
	function onOrgChange(item: OrgPublic | undefined) {
		org = item;
	}
	function renderActivity(item: TreePublic) {
		return item.name;
	}
	function onActivityChange(item: TreePublic | undefined) {
		activity = item;
	}
</script>

<div class="bg-background p-4 text-foreground">
	<div class="space-y-5">
		<div class="grid grid-rows-4 gap-4">
			<div class="rounded-lg bg-background p-4 text-foreground">default</div>
			<div class="rounded-lg bg-primary p-4 text-primary-foreground">primary</div>
			<div class="rounded-lg bg-secondary p-4 text-secondary-foreground">secondary</div>
			<div class="rounded-lg bg-accent p-4 text-accent-foreground">accent</div>
			<div class="bg-outline text-outline-foreground rounded-lg p-4">outline</div>
			<div class="rounded-lg bg-destructive p-4 text-destructive-foreground">destructive</div>
			<div class="rounded-lg bg-muted p-4 text-muted-foreground">muted</div>
			<div class="rounded-lg bg-card p-4 text-card-foreground">card</div>
		</div>
	</div>
</div>

<div class="grid grid-cols-3 gap-4">
	<div
		class="preview flex min-h-[350px] w-full items-center justify-center rounded bg-slate-300 p-10"
	>
		<Autocomplete
			title="Organisation"
			read={orgsReadOrgs}
			renderItem={renderOrg}
			onValueChange={onOrgChange}
		/>

		<Autocomplete
			title="Acteurs"
			read={peopleReadPeople}
			renderItem={renderActivity}
			onValueChange={onActivityChange}
		/>
		<Autocomplete
			title="Activités"
			read={activitiesReadActivities}
			renderItem={renderActivity}
			onValueChange={onActivityChange}
		/>
	</div>
	<div></div>
	<div></div>
</div>
