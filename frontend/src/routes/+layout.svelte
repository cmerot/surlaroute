<script lang="ts">
	import { navigating } from "$app/state";
	import Layout from "$lib/components/layout/layout.svelte";
	import { auth } from "$lib/stores/auth";
	import type { Snippet } from "svelte";
	import "../app.css";
	import type { LayoutData } from "./$types";

	type Props = { children: Snippet; data: LayoutData };

	const { children, data }: Props = $props();

	let opacity = $state("opacity-0");

	$effect(() => {
		// Show loading bar when navigation is in progress (from and to are not null)
		opacity = navigating?.from && navigating?.to ? "opacity-100" : "opacity-0";
	});

	// Separate effect for auth logic
	$effect(() => {
		if (data.user && data.authToken) {
			auth.login(data.user, data.authToken);
		} else {
			auth.logout();
		}
	});
</script>

<div
	class="loading-bar fixed inset-x-0 top-0 z-50 h-1 bg-couleur-bg transition-opacity duration-300 {opacity}"
></div>

<Layout>
	<div class="flex h-full bg-white/50 dark:bg-black/50">
		<div class="grow">
			{@render children()}
		</div>
	</div>
</Layout>

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
