import { Account, Directory, Home, Tour, Users } from "$lib/components/icons";
import type { Nav } from "$lib/types/nav.js";
import { ChartLine, Map as LucidMap } from "lucide-svelte";

type NavConfig = {
	mainNav: Nav;
	adminNav: Nav;
	userNav: Nav;
};

export const navConfig: NavConfig = {
	mainNav: {
		items: [
			{ title: "Accueil", href: "/", icon: Home },
			{ title: "Explorer", href: "/explore", icon: LucidMap },
			{ title: "Tournées", href: "/tours", icon: Tour },
			{
				title: "Annuaire",
				href: "/directory",
				icon: Directory,
			},
		],
	},
	adminNav: {
		title: "Admin",
		items: [
			{ title: "Dashboard", href: "/admin", icon: ChartLine },
			{ title: "Tournées", href: "/admin/tours", icon: Tour },
			{
				title: "Utilisateurs",
				href: "/admin/users",
				icon: Users,
			},
			{
				title: "Annuaire",
				href: "/admin/directory",
				icon: Directory,
			},
		],
	},
	userNav: {
		title: "Mes donnée",
		items: [{ title: "Mon compte", href: "/me", icon: Account }],
	},
};
