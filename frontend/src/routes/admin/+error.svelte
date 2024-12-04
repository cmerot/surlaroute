<script lang="ts">
	import { page } from '$app/stores';
</script>

<div
	style="background-size: 100% 100%;
background-position: 0px 0px,0px 0px;
background-image: radial-gradient(74% 86% at 72% 38%, #06A206F5 0%, #C2C837F5 100%),radial-gradient(75% 75% at 50% 50%, #00FFFFFF 0%, #8006A2F5 100%);"
>
	<div class="flex h-screen items-center justify-center">
		<section
			class="w-full space-y-10 bg-background/30 p-10 text-center text-foreground sm:w-[640px]"
		>
			<h1 class="mb-3 text-3xl font-bold">
				Oups! {$page.status}<br />
				<small class="text-foreground/80"> {$page.error?.message} </small>
			</h1>
		</section>
	</div>
</div>
