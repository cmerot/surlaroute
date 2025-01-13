<script>
import DisciplineBadge from "$lib/components/discipline-badge/discipline-badge.svelte";
import { Mobility } from "$lib/components/icons";
import MobilityBadge from "$lib/components/mobility-badge/mobility-badge.svelte";
import Section from "../section.svelte";
</script>

<Section name="mobilities" title="Mobilités" class="space-y-10">
	<h3 class="mb-4 font-bold">Badges et icones</h3>

	<div class="flex gap-4">
		<div class="space-y-2">
			<Mobility mobility={{ name: "Bateau", path: "Bateau" }} />
			<MobilityBadge mobility={{ name: "Bateau", path: "Bateau" }} />
		</div>
		<div class="space-y-2">
			<Mobility mobility={{ name: "Équestre", path: "Equestre" }} />
			<MobilityBadge mobility={{ name: "Équestre", path: "Equestre" }} />
		</div>
		<div class="space-y-2">
			<Mobility mobility={{ name: "Marche", path: "Marche" }} />
			<MobilityBadge mobility={{ name: "Marche", path: "Marche" }} />
		</div>
		<div class="space-y-2">
			<Mobility mobility={{ name: "Vélo", path: "Velo" }} />
			<MobilityBadge mobility={{ name: "Vélo", path: "Velo" }} />
		</div>
	</div>
</Section>

<Section name="disciplines" title="Disciplines">
	<DisciplineBadge discipline={{ name: "Musique", path: "Musique" }} />
</Section>
