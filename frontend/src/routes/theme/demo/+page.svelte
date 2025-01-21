<script>
	import DisciplineBadge from "$lib/components/discipline-badge/discipline-badge.svelte";
	import { Activity, MapPin, Mobility } from "$lib/components/icons";
	import MobilityBadge from "$lib/components/mobility-badge/mobility-badge.svelte";
	import { Button } from "$lib/components/ui/button";
	import Section from "../section.svelte";
</script>

<hr class="my-10" />
<Section name="mobilities" title="Mobilités" class="sdpace-y-10">
	<h3 class="mb-4 font-bold">Badges, icônes et boutons</h3>
	<div class="flex gap-4">
		<div class="space-y-2">
			<Mobility mobility={{ name: "Bateau", path: "Bateau" }} />
			<MobilityBadge mobility={{ name: "Bateau", path: "Bateau" }} />
			<Button variant="Bateau" size="icon">
				<Mobility mobility={{ name: "Bateau", path: "Bateau" }} />
			</Button>
		</div>
		<div class="space-y-2">
			<Mobility mobility={{ name: "Équestre", path: "Equestre" }} />
			<MobilityBadge mobility={{ name: "Équestre", path: "Equestre" }} />
			<Button variant="Equestre" size="icon">
				<Mobility mobility={{ name: "Équestre", path: "Equestre" }} />
			</Button>
		</div>
		<div class="space-y-2">
			<Mobility mobility={{ name: "Marche", path: "Marche" }} />
			<MobilityBadge mobility={{ name: "Marche", path: "Marche" }} />
			<Button variant="Marche" size="icon">
				<Mobility mobility={{ name: "Marche", path: "Marche" }} />
			</Button>
		</div>
		<div class="space-y-2">
			<Mobility mobility={{ name: "Vélo", path: "Velo" }} />
			<MobilityBadge mobility={{ name: "Vélo", path: "Velo" }} />
			<Button variant="Velo" size="icon">
				<Mobility mobility={{ name: "Vélo", path: "Velo" }} />
			</Button>
		</div>
	</div>
</Section>

<hr class="my-10" />

<Section name="disciplines" title="Disciplines">
	<h3 class="mb-4 font-bold">Badges</h3>
	<DisciplineBadge discipline={{ name: "Musique", path: "Musique" }} />
</Section>

<hr class="my-10" />

<Section name="categories" title="Catégories">
	<h3 class="mb-4 font-bold">Icônes</h3>
	<div class="flex gap-4">
		<div class="space-y-2">
			Production
			<Activity activity={{ name: "Production", path: "Structure.Production" }} />
			<MapPin size="48" activity={{ name: "Production", path: "Structure.Production" }} />
		</div>
		<div class="space-y-2">
			Diffusion
			<Activity activity={{ name: "Diffusion", path: "Structure.Diffusion" }} />
			<MapPin size="48" activity={{ name: "Diffusion", path: "Structure.Diffusion" }} />
		</div>
		<div class="space-y-2">
			Ressource
			<Activity activity={{ name: "Ressource", path: "Structure.Ressource" }} />
			<MapPin size="48" activity={{ name: "Ressource", path: "Structure.Ressource" }} />
		</div>
		<div class="space-y-2">
			Default
			<Activity activity={{ name: "Robinet", path: "Robinet" }} />
			<MapPin size="48" activity={{ name: "Robinet", path: "Robinet" }} />
		</div>
	</div>
</Section>
