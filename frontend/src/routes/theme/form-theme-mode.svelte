<script lang="ts">
	import { Label } from "$lib/components/ui/label";
	import * as RadioGroup from "$lib/components/ui/radio-group";
	import { mode, setMode, setTheme, systemPrefersMode, theme } from "mode-watcher";
</script>

<div class="mb-4 flex space-x-4">
	<div class="flex-none">
		<h2 class="mb-2 font-bold">Mode</h2>
		<RadioGroup.Root value={$mode} onValueChange={(v) => setMode(v as "light" | "dark" | "system")}>
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
				<RadioGroup.Item value="nb" id="nb" />
				<Label for="nb">nb</Label>
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
