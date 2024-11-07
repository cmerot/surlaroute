import { redirect } from '@sveltejs/kit';
import { client, loginTestToken } from '$lib/backend/client/services.gen';
import { sessionStore } from '$lib/server/sessionStore.js';

export async function load({ cookies, url }) {
	const session = sessionStore.get(cookies.get('sessionId') || '');
	const accessToken = session?.data?.access_token;

	if (!accessToken) {
		redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	client.setConfig({
		headers: {
			Authorization: `Bearer ${accessToken}`
		}
	});

	const { error } = await loginTestToken();
	if (error) {
		redirect(303, `/login?redirectTo=${url.pathname}`);
	}
}
