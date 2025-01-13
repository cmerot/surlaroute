<script lang="ts">
import { Bateau, Equestre, Logo, Marche, Velo } from "$lib/components/icons";
import * as Page from "$lib/components/page";
import Declinaison from "./declinaison.svelte";
import Section from "./section.svelte";
import ThemeSample from "./theme-sample.svelte";
</script>

<Page.Root title="Theme" id="page">
	<Page.Title>Thème</Page.Title>
	<Page.Content class="space-y-20">
		<ul class="list-inside list-disc">
			<li><a class="underline" href="#versions">Versions</a></li>
			<li><a class="underline" href="#decli">Déclinaisons</a></li>
			<li><a class="underline" href="#themes">Thème et mode</a></li>
			<!-- <li><a class="underline" href="#couleurs">Couleurs</a></li> -->
		</ul>
		<Section name="version">
			<div class="grid grid-cols-2">
				<div
					class="relative flex h-[400px] items-center justify-center bg-couleur-bg text-couleur-fg"
				>
					<h1 class="absolute left-0 top-0 p-10 font-logo text-3xl">
						Version Couleur
					</h1>
					<Logo size="40%" />
				</div>
				<div
					class="relative flex h-[400px] items-center justify-center bg-nb-bg text-nb-fg"
					style="font-color: white"
				>
					<h1 class="absolute left-0 top-0 p-10 font-logo text-3xl">
						Version Noir & Blanc
					</h1>
					<Logo size="40%" />
				</div>
				<div
					class="relative flex h-[400px] items-center justify-center bg-neg-bg text-neg-fg"
				>
					<h1 class="absolute left-0 top-0 p-10 font-logo text-3xl">
						Version Negative
					</h1>
					<Logo size="40%" />
				</div>
				<div
					class="relative flex h-[400px] items-center justify-center bg-gris-bg text-gris-fg"
				>
					<h1 class="absolute left-0 top-0 p-10 font-logo text-3xl">
						Version niveau de gris
					</h1>
					<Logo size="40%" />
				</div>
				<div
					class="relative flex h-[400px] items-center justify-center bg-nb-bg"
				>
					<h1
						class="absolute left-0 top-0 p-10 font-logo text-3xl"
						style="color:#BC002D"
					>
						Version Japon
					</h1>
					<Logo size="40%" background="#BC002D" class="text-white" />
				</div>
			</div>
		</Section>
		<Section name="decli" title="Déclinaisons">
			<div class="grid grid-cols-4 gap-4">
				<Declinaison Icon={Bateau} name="bateau" />
				<Declinaison Icon={Equestre} name="equestre" />
				<Declinaison Icon={Velo} name="velo" />
				<Declinaison Icon={Marche} name="marche" />
			</div>
		</Section>
		<Section name="themes" title="Thème et mode" class="space-y-4">
			<div class="grid grid-cols-6 gap-4">
				<ThemeSample mode="light" />
				<ThemeSample mode="dark" />
				<ThemeSample theme="nb" />
				<ThemeSample theme="vert" />
				<ThemeSample theme="marron" />
			</div>
			<div class="grid grid-cols-6 gap-4">
				<ThemeSample mode="light" theme="nb" />
				<ThemeSample mode="dark" theme="nb" />
				<ThemeSample mode="light" theme="vert" />
				<ThemeSample mode="dark" theme="vert" />
				<ThemeSample mode="light" theme="marron" />
				<ThemeSample mode="dark" theme="marron" />
			</div>
		</Section>
		<!-- <Section name="couleurs" title="Couleurs">
			<div class="grid grid-cols-4">
				<ColorSet name="oregon" />
				<ColorSet name="thistle-green" />
				<ColorSet name="gumbo" />
				<ColorSet name="faded-jade" />
			</div>
		</Section> -->
	</Page.Content>
</Page.Root>
