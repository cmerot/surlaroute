<script lang="ts">
	import { page } from "$app/state";

	const bgs = {
		4: "background-image: radial-gradient(74% 86% at 72% 38%, #FF8C00F5 0%, #D2691EF5 100%),radial-gradient(75% 75% at 50% 50%, #00FFFFFF 0%, #8B4513F5 100%);",
		5: "background-image: radial-gradient(74% 86% at 72% 38%, #FF0000F5 0%, #8B0000F5 100%),radial-gradient(75% 75% at 50% 50%, #00FFFFFF 0%, #660000F5 100%);",
	};
	let style = bgs[5];
	if (page.status < 500) {
		style = bgs[4];
	}
</script>

<div class="flex h-full items-center justify-center" {style}>
	<section class="w-full space-y-10 bg-background/30 p-10 text-foreground sm:w-[640px]">
		<h1 class="text-3xl font-bold">
			Erreur {page.status}<br />
		</h1>
		<p class="text-xl text-foreground/80">{page.error?.message}</p>
	</section>
</div>
