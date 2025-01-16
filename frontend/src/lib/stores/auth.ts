import { browser } from "$app/environment";
import type { UserPublic } from "$lib/backend/client";
import { writable } from "svelte/store";

interface AuthState {
	user: UserPublic | null;
	authToken: string | null;
}

function createAuthStore() {
	const { subscribe, set } = writable<AuthState>({
		user: null,
		authToken: null,
	});

	// Initialize from localStorage if we're in the browser
	if (browser) {
		const stored = localStorage.getItem("auth");
		if (stored) set(JSON.parse(stored));
	}

	return {
		subscribe,
		login: (user: UserPublic, authToken: string) => {
			set({ user, authToken });
			if (browser) {
				localStorage.setItem("auth", JSON.stringify({ user, authToken }));
			}
		},
		logout: () => {
			set({ user: null, authToken: null });
			if (browser) {
				localStorage.removeItem("auth");
			}
		},
	};
}

export const auth = createAuthStore();
