import { client } from "$lib/backend/client";
import { sessionStore } from "$lib/server/sessionStore";
import type { Handle } from "@sveltejs/kit";

const VITE_API_URL = import.meta.env.VITE_API_URL;

export const handle: Handle = async ({ event, resolve }) => {
	const sessionId = event.cookies.get("sessionId");

	if (sessionId) {
		const session = sessionStore.get(sessionId);
		event.locals.user = session?.data?.user;
		event.locals.authToken = session?.data?.authToken;
	}

	return await resolve(event);
};

function initializeServer() {
	client.setConfig({ baseUrl: VITE_API_URL });
}

initializeServer();
