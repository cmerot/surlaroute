<script lang="ts">
	import { Bateau, Equestre, Marche, Velo } from "$lib/components/icons";
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	import { InputSearch } from "$lib/components/input-search";
	import { Button } from "$lib/components/ui/button";
	import { cn } from "$lib/utils.js";
	import type { HTMLAttributes } from "svelte/elements";
	import type { Results } from "../utils";
	import TourFeatureList from "./tour-feature-list.svelte";

	type Props = HTMLAttributes<HTMLDivElement> & {
		q?: string;
		selectedTourId?: string;
		selectedMarkerId?: string;
		apiResults: Results; // weird ts conflict when prop is named "results", has to do with HTMLAttributes<HTMLDivElement>
		showActors?: boolean;
		mobilityPath?: string;
	};

	let {
		q = $bindable(),
		selectedTourId = $bindable(),
		selectedMarkerId = $bindable(),
		class: className,
		apiResults: results,
		showActors = $bindable(),
		mobilityPath = $bindable(),
		...restProps
	}: Props = $props();

	let q_unsubmitted: string = $state(q || "");
	let hasScroll = $state(false);

	let contentDiv: HTMLDivElement;
	function checkScroll() {
		hasScroll = contentDiv?.scrollTop > 0;
	}
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	function onsubmit(event: Event) {
		event.preventDefault();
		q = q_unsubmitted;
	}

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

<div class={cn("flex flex-col bg-background", className)} {...restProps}>
	<div class="p-3 transition-shadow {hasScroll ? 'shadow-md' : 'border-b'}">
		<!-- <form data-sveltekit-keepfocus {onsubmit}>
			<InputSearch name="q" bind:value={q_unsubmitted} autocomplete="off" />
		</form> -->
		<h3 class="text-lg">Tournées</h3>
		<Button
			variant="Bateau"
			size="icon"
			class={isMobilitySelected("Bateau") ? "" : "opacity-50"}
			onclick={() => toggleMobility("Bateau")}
		>
			<Bateau />
		</Button>
		<Button
			variant="Equestre"
			size="icon"
			class={isMobilitySelected("Equestre") ? "" : "opacity-50"}
			onclick={() => toggleMobility("Equestre")}
		>
			<Equestre />
		</Button>
		<Button
			variant="Marche"
			size="icon"
			class={isMobilitySelected("Marche") ? "" : "opacity-50"}
			onclick={() => toggleMobility("Marche")}
		>
			<Marche />
		</Button>
		<Button
			variant="Velo"
			size="icon"
			class={isMobilitySelected("Velo") ? "" : "opacity-50"}
			onclick={() => toggleMobility("Velo")}
		>
			<Velo />
		</Button>
	</div>
	<div bind:this={contentDiv} onscroll={checkScroll} class="min-h-0 flex-1 overflow-y-auto">
		<TourFeatureList
			results={results.slr}
			bind:selectedTourId
			bind:selectedMarkerId
			bind:showActors
		/>
	</div>
</div>
