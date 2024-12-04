<script>
	import { buttonVariants } from '$lib/components/ui/button';
</script>

<div class="bg-gradient-to-br from-purple-500 to-pink-500 dark:from-purple-950 dark:to-pink-950">
	<div class="flex h-screen items-center justify-center">
		<section
			class="w-full space-y-10 rounded-none bg-background/70 p-10 text-center text-foreground sm:w-[640px] sm:rounded-xl"
		>
			<header>
				<h1 class="mb-3 text-3xl font-bold uppercase">Sur la route</h1>
				<p class="text-center text-foreground">
					L'atlas des tournées artistiques à modes doux, <br />un projet du réseau ArMoDo - les Arts
					en Mode Doux
				</p>
			</header>
			<section>
				<p class="text-center">
					<a href="/admin" class={buttonVariants({ variant: 'secondary', size: 'lg' })}>
						Accéder au tableau de bord
					</a>
				</p>
			</section>
		</section>
	</div>
</div>
