<script lang="ts">
	import { Bateau, Equestre, Marche, Velo } from "$lib/components/icons";
	import { Button } from "$lib/components/ui/button";
	import { Label } from "$lib/components/ui/label/index.js";
	import { Switch } from "$lib/components/ui/switch/index.js";
	import { cn } from "$lib/utils.js";
	import type { HTMLAttributes } from "svelte/elements";

	type Props = HTMLAttributes<HTMLDivElement> & {
		mobilityPath?: string;
		searchInBounds?: boolean;
	};

	let {
		class: className,
		mobilityPath = $bindable(),
		searchInBounds = $bindable(false),
		...restProps
	}: Props = $props();

	function isFilteredByMobility() {
		return mobilityPath && mobilityPath != "";
	}

	function isMobilitySelected(path: string) {
		if (!isFilteredByMobility()) return true;
		return path === mobilityPath;
	}

	function toggleMobility(path: string) {
		if (isFilteredByMobility() && isMobilitySelected(path)) mobilityPath = undefined;
		else mobilityPath = path;
	}
</script>

<div class={cn(``, className)} {...restProps}>
	<Button
		variant="Bateau"
		size="icon"
		class="{isMobilitySelected('Bateau')
			? 'ring-4 ring-couleur-dark'
			: ''} flex-none [&_svg]:size-6"
		onclick={() => toggleMobility("Bateau")}
	>
		<Bateau />
	</Button>
	<Button
		variant="Equestre"
		size="icon"
		class="{isMobilitySelected('Equestre')
			? 'ring-4 ring-couleur-dark'
			: ''} flex-none [&_svg]:size-6"
		onclick={() => toggleMobility("Equestre")}
	>
		<Equestre />
	</Button>
	<Button
		variant="Marche"
		size="icon"
		class="{isMobilitySelected('Marche')
			? 'ring-4 ring-couleur-dark'
			: ''} flex-none [&_svg]:size-6"
		onclick={() => toggleMobility("Marche")}
	>
		<Marche />
	</Button>
	<Button
		variant="Velo"
		size="icon"
		class="{isMobilitySelected('Velo') ? 'ring-4 ring-couleur-dark' : ''} flex-none [&_svg]:size-6"
		onclick={() => toggleMobility("Velo")}
	>
		<Velo />
	</Button>
	<span class="flex flex-none items-center gap-2">
		<Switch id="search-in-bounds" bind:checked={searchInBounds} />
		<Label for="search-in-bounds">Suivre la carte</Label>
	</span>
</div>
