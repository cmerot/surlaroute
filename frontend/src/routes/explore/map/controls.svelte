<script lang="ts">
	import * as Select from "$lib/components/ui/select";
	import { Layers } from "lucide-svelte";
	import {
		AttributionControl,
		Control,
		ControlButton,
		ControlGroup,
		NavigationControl,
		ScaleControl,
	} from "svelte-maplibre";
	import SelectTrigger from "./select-trigger.svelte";
	import { styles } from "./styles";

	let { styleName = $bindable() } = $props();
</script>

<ScaleControl position="bottom-left" />
<AttributionControl position="bottom-right" />

<Control position="bottom-right">
	<ControlGroup>
		<Select.Root type="single" bind:value={styleName as string}>
			<SelectTrigger>
				<ControlButton>
					<Layers size="20" color="black" strokeWidth={2.5} />
				</ControlButton>
			</SelectTrigger>
			<Select.Content>
				{#each Object.keys(styles) as k}
					<Select.Item value={k as string}>{styles[k].title}</Select.Item>
				{/each}
			</Select.Content>
		</Select.Root>
	</ControlGroup>
</Control>
<NavigationControl position="bottom-right" />
