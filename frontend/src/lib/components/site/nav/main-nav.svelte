<script lang="ts">
	import * as Icon from "$lib/components/icons/index.js";

	const { title }: { title: string } = $props();
</script>

<nav class="flex items-center gap-6 text-sm">
	<a href="/" class="ml-4 flex items-center gap-2 text-primary md:ml-0">
		<Icon.Logo class="size-8" />
		<span class="mt-1 font-logo text-2xl">
			{title}
		</span>
	</a>
</nav>
