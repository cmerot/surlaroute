<script lang="ts">
	import type { ActorSummaryPublic, TreePublic } from '$lib/backend/client';
	import { activitiesReadActivities, directoryGetActors } from '$lib/backend/client';
	import Autocomplete from '$lib/components/autocomplete/autocomplete.svelte';

	let activity = $state<TreePublic>();
	function renderActor(actor: ActorSummaryPublic) {
		return actor.name;
	}
	function renderActivity(item: TreePublic) {
		return item.name;
	}
	function onActivityChange(item: TreePublic | undefined) {
		activity = item;
	}
	function onActorChange(item: TreePublic | undefined) {
		activity = item;
	}
</script>

<div class="grid grid-cols-3 gap-4">
	<div
		class="preview flex min-h-[350px] w-full items-center justify-center rounded bg-slate-300 p-10"
	>
		<!-- renderItem={renderActor} -->
		<Autocomplete title="Acteurs" read={directoryGetActors} onValueChange={onActorChange} />
		<Autocomplete
			title="Activités"
			read={activitiesReadActivities}
			renderItem={renderActivity}
			onValueChange={onActivityChange}
		/>
	</div>
</div>
