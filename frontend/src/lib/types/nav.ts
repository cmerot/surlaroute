import type { Icon as IconType } from "lucide-svelte";
export type NavItem = {
	title?: string;
	href?: string;
	disabled?: boolean;
	external?: boolean;
	icon?: typeof IconType;
	active?: boolean;
};
export type Nav = NavItem & {
	title?: string;
	items: NavItem[];
};
