<script lang="ts">
	import type { TourFeatureCollection } from "$lib/backend/client";
	import { cn } from "$lib/utils.js";
	import type { HTMLAttributes } from "svelte/elements";
	import TourList from "./tour-list.svelte";

	type Props = HTMLAttributes<HTMLDivElement> & {
		selectedTourId?: string;
		selectedMarkerId?: string;
		tourFeatureCollections: TourFeatureCollection[];
		showActors?: boolean;
		mobilityPath?: string;
		searchInBounds?: boolean;
	};

	let {
		selectedTourId = $bindable(),
		selectedMarkerId = $bindable(),
		class: className,
		tourFeatureCollections,
		showActors = $bindable(),
		mobilityPath = $bindable(),
		searchInBounds = $bindable(false),
		...restProps
	}: Props = $props();
</script>

<div class={cn("flex h-full flex-col bg-background", className)} {...restProps}>
	<div class="shadow">
		<h1 class="p-6 font-bold">Tournées</h1>
	</div>
	<div class="overflow-auto">
		<TourList
			tours={tourFeatureCollections}
			bind:selectedTourId
			bind:selectedMarkerId
			bind:showActors
		/>
	</div>
</div>
