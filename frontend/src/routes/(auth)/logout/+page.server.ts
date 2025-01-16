import { sessionStore } from "$lib/server/sessionStore.js";
import { redirect } from "@sveltejs/kit";
import type { Actions } from "./$types.js";

export const actions: Actions = {
	default: async ({ cookies }) => {
		const sessionId = cookies.get("sessionId");

		if (sessionId) {
			sessionStore.destroy(sessionId);
			cookies.delete("sessionId", { path: "/" });
		}

		redirect(303, "/");
	},
};
