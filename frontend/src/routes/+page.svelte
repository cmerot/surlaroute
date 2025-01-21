<script>
	import { Logotext } from "$lib/components/icons";
	import * as Page from "$lib/components/page";
	import { Button } from "$lib/components/ui/button";
</script>

<Page.Root>
	<Page.Content class=" bg-couleur-bg text-couleur-fg">
		<Logotext class="mx-auto mb-3 size-64" />
		<div class="m-auto space-y-8 text-couleur-fg">
			<h1 class="px-2 text-center text-xl md:text-2xl">
				L'atlas des tournées artistiques à modes doux
			</h1>
			<p class="text-center">
				<Button href="/explore" variant="secondary" class="rounded text-xl" size="lg">
					Explorer
				</Button>
			</p>
			<div class="prose m-auto text-lg text-couleur-fg">
				<p>
					Le mouvement des arts à modes doux se développe partout en Europe. Des centaines
					d’artistes et de compagnies ont choisi, pour réduire leur empreinte environnementale, de
					tourner leurs spectacles en mobilités douces : à vélo, à cheval, à pieds ou à la voile.
				</p>
				<p>
					« Sur la route » est un projet imaginé par Slowfest et le réseau ARMODO pour recenser et
					cartographier les tournées artistiques en mobilités douces. C’est une plateforme
					collaborative et numérique dont les objectifs sont :
				</p>
				<ul>
					<li>🔆 Visibiliser et valoriser les tournées en modes doux.</li>
					<li>
						🔆 Faire baisser les temps de production et susciter des vocations par la mutualisation
						des données.
					</li>
					<li>
						🔆 Accélérer la mutualisation de matériel spécifique aux modes doux (vélogistique,
						autonomie énergétique).
					</li>
				</ul>
				<p>
					Slowfest est en partenariat avec les réseaux ARMODO et <a
						href="https://www.linkedin.com/company/european-network-of-cultural-centers/"
					>
						European Network of Cultural Centres
					</a>
					pour ce projet, soutenu par la
					<a href="https://www.linkedin.com/company/conseil-r-gional-nouvelle-aquitaine/">
						Région Nouvelle-Aquitaine
					</a>
					au titre de la sobriété numérique et l’Union Européenne pour le programme
					<a href="https://www.linkedin.com/company/livemx/">LIVEMX</a>.
				</p>
				<hr />
				<ul class="m-auto">
					<li>
						<a href="https://www.slowfest.org/" class=" text-white no-underline">
							<span class="no-underline">Slowfest</span><br />
							<span class="no-underline opacity-40">https://www.slowfest.org/</span>
						</a>
					</li>
					<li>
						<a href="https://www.armodo.org/" class=" text-white no-underline">
							<span class="no-underline">ArMoDo</span><br />
							<span class="no-underline opacity-40">https://www.armodo.org/</span>
						</a>
					</li>
				</ul>
			</div>
		</div>
	</Page.Content>
</Page.Root>
