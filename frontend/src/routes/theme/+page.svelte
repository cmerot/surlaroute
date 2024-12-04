<script lang="ts">
	import { Label } from '$lib/components/ui/label';
	import * as RadioGroup from '$lib/components/ui/radio-group';
	import { mode, setMode, setTheme, systemPrefersMode, theme } from 'mode-watcher';
	import Colors from './colors.svelte';
</script>

<div class="p-4">
	<div class="space-y-4">
		<h1 class="text-3xl font-bold">Appearence</h1>
		<div class="flex space-x-4">
			<div class="flex-none">
				<h2 class="mb-2 font-bold">Mode</h2>
				<RadioGroup.Root
					value={$mode}
					onValueChange={(v) => setMode(v as 'light' | 'dark' | 'system')}
				>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="light" id="m1" />
						<Label for="m1">light</Label>
					</div>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="dark" id="m2" />
						<Label for="m2">dark</Label>
					</div>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="system" id="system" />
						<Label for="system">system ({$systemPrefersMode})</Label>
					</div>
				</RadioGroup.Root>
			</div>
			<div class="flex-none">
				<h2 class="mb-2 font-bold">Theme</h2>
				<RadioGroup.Root value={$theme} onValueChange={setTheme}>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="violet" id="violet" />
						<Label for="violet">violet</Label>
					</div>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="vert" id="vert" />
						<Label for="vert">vert</Label>
					</div>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="marron" id="marron" />
						<Label for="marron">marron</Label>
					</div>
				</RadioGroup.Root>
			</div>
		</div>
	</div>
	<div class="mt-4 grid grid-cols-6 gap-4">
		<Colors mode="light" />
		<Colors mode="dark" />
		<Colors theme="violet" />
		<Colors theme="vert" />
		<Colors theme="marron" />
	</div>
	<div class="mt-4 grid grid-cols-6 gap-4">
		<Colors mode="light" theme="violet" />
		<Colors mode="dark" theme="violet" />
		<Colors mode="light" theme="vert" />
		<Colors mode="dark" theme="vert" />
		<Colors mode="light" theme="marron" />
		<Colors mode="dark" theme="marron" />
	</div>
	<div class="mt-4 grid grid-cols-4 gap-4">
		<div>
			<div class="rounded-t-lg bg-oregon-500 p-4">Oregon</div>
			<div class="bg-oregon-50 p-4">oregon-50</div>
			<div class="bg-oregon-100 p-4">oregon-100</div>
			<div class="bg-oregon-200 p-4">oregon-200</div>
			<div class="bg-oregon-300 p-4">oregon-300</div>
			<div class="bg-oregon-400 p-4">oregon-400</div>
			<div class="bg-oregon-500 p-4">oregon-500</div>
			<div class="bg-oregon-600 p-4">oregon-600</div>
			<div class="bg-oregon-700 p-4">oregon-700</div>
			<div class="bg-oregon-800 p-4">oregon-800</div>
			<div class="rounded-b-lg bg-oregon-900 p-4">oregon-900</div>
		</div>
		<div>
			<div class="rounded-t-lg bg-thistle-green-500 p-4">Thistle Green</div>
			<div class="bg-thistle-green-50 p-4">thistle-green-50</div>
			<div class="bg-thistle-green-100 p-4">thistle-green-100</div>
			<div class="bg-thistle-green-200 p-4">thistle-green-200</div>
			<div class="bg-thistle-green-300 p-4">thistle-green-300</div>
			<div class="bg-thistle-green-400 p-4">thistle-green-400</div>
			<div class="bg-thistle-green-500 p-4">thistle-green-500</div>
			<div class="bg-thistle-green-600 p-4">thistle-green-600</div>
			<div class="bg-thistle-green-700 p-4">thistle-green-700</div>
			<div class="bg-thistle-green-800 p-4">thistle-green-800</div>
			<div class="rounded-b-lg bg-thistle-green-900 p-4">thistle-green-900</div>
		</div>
		<div>
			<div class="rounded-t-lg bg-gumbo-500 p-4">Gumbo</div>
			<div class="bg-gumbo-50 p-4">gumbo-50</div>
			<div class="bg-gumbo-100 p-4">gumbo-100</div>
			<div class="bg-gumbo-200 p-4">gumbo-200</div>
			<div class="bg-gumbo-300 p-4">gumbo-300</div>
			<div class="bg-gumbo-400 p-4">gumbo-400</div>
			<div class="bg-gumbo-500 p-4">gumbo-500</div>
			<div class="bg-gumbo-600 p-4">gumbo-600</div>
			<div class="bg-gumbo-700 p-4">gumbo-700</div>
			<div class="bg-gumbo-800 p-4">gumbo-800</div>
			<div class="rounded-b-lg bg-gumbo-900 p-4">gumbo-900</div>
		</div>
		<div>
			<div class="rounded-t-lg bg-faded-jade-500 p-4">Faded Jade</div>
			<div class="bg-faded-jade-50 p-4">faded-jade-50</div>
			<div class="bg-faded-jade-100 p-4">faded-jade-100</div>
			<div class="bg-faded-jade-200 p-4">faded-jade-200</div>
			<div class="bg-faded-jade-300 p-4">faded-jade-300</div>
			<div class="bg-faded-jade-400 p-4">faded-jade-400</div>
			<div class="bg-faded-jade-500 p-4">faded-jade-500</div>
			<div class="bg-faded-jade-600 p-4">faded-jade-600</div>
			<div class="bg-faded-jade-700 p-4">faded-jade-700</div>
			<div class="bg-faded-jade-800 p-4">faded-jade-800</div>
			<div class="rounded-b-lg bg-faded-jade-900 p-4">faded-jade-900</div>
		</div>
	</div>
</div>

<!--
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
</div> -->
