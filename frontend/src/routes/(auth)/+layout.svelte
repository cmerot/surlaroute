<script lang="ts">
	let { children } = $props();
</script>

<div class="bg-gradient-to-br from-purple-500 to-pink-500 dark:from-purple-950 dark:to-pink-950">
	<div class="flex h-screen items-center justify-center">
		<section
			class="w-full space-y-10 rounded-md bg-background bg-opacity-90 p-10 text-foreground sm:w-[640px]"
		>
			{@render children()}
		</section>
	</div>
</div>
