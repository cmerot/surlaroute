<script lang="ts">
	import clsx from "clsx";
	import type { SvelteHTMLElements } from "svelte/elements";

	type Props = SvelteHTMLElements["div"] & {
		loading?: boolean;
	};

	let { loading = false, class: classNames, ...restProps }: Props = $props();
</script>

{#if loading}
	<div
		class={clsx(
			"loading-bar fixed inset-x-0 top-0 z-50 h-1 bg-couleur-bg transition-opacity duration-300",
			classNames,
		)}
		{...restProps}
	></div>
{/if}

<style>
	.loading-bar {
		animation: loading 2s ease-in-out infinite;
	}

	@keyframes loading {
		0% {
			width: 0%;
			margin-left: 0%;
		}
		50% {
			width: 50%;
			margin-left: 25%;
		}
		100% {
			width: 0%;
			margin-left: 100%;
		}
	}
</style>
