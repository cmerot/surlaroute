<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';

	const { mode, theme }: { mode?: string; theme?: string } = $props();
</script>

<div class="{mode} rounded-lg">
	<div class=" {theme} rounded-lg border p-4">
		<h2 class="text-lg font-bold">{mode}&nbsp;{theme}</h2>
		<div class="mt-2 space-y-2">
			<Button variant="default" class="w-full">Primary</Button>
			<Button variant="secondary" class="w-full">Secondary</Button>
			<Button variant="outline" class="w-full">Outline</Button>
			<Button variant="destructive" class="w-full">Destructive</Button>
			<Button variant="link" class="w-full">Link</Button>
			<Button variant="ghost" class="w-full">Ghost</Button>
			<div class="rounded-md bg-accent p-2.5 text-center text-sm text-accent-foreground">
				Accent
			</div>
			<div class="rounded-md bg-muted p-2.5 text-center text-sm text-muted-foreground">Muted</div>
			<div class="rounded-md bg-card p-2.5 text-center text-sm text-card-foreground">Card</div>
		</div>
	</div>
</div>
