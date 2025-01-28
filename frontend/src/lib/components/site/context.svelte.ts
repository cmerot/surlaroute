import { IsMobile } from "$lib/hooks/is-mobile.svelte.js";
import { getContext, setContext } from "svelte";

class SidebarState {
	#isMobile: IsMobile;

	constructor() {
		this.#isMobile = new IsMobile();
	}

	// Convenience getter for checking if the sidebar is mobile
	// without this, we would need to use `sidebar.isMobile.current` everywhere
	get isMobile() {
		return this.#isMobile.current;
	}
}

const SYMBOL_KEY = "slr-sidebar";

/**
 * Instantiates a new `SidebarState` instance and sets it in the context.
 *
 * @param props The constructor props for the `SidebarState` class.
 * @returns  The `SidebarState` instance.
 */
export function setSidebar(): SidebarState {
	return setContext(Symbol.for(SYMBOL_KEY), new SidebarState());
}

/**
 * Retrieves the `SidebarState` instance from the context. This is a class instance,
 * so you cannot destructure it.
 * @returns The `SidebarState` instance.
 */
export function useSidebar(): SidebarState {
	return getContext(Symbol.for(SYMBOL_KEY));
}
