import type { Handle } from '@sveltejs/kit';
import { randomBytes } from 'crypto';
import { sessionStore } from '$lib/server/sessionStore';
import { client } from '$lib/backend/client';

const VITE_API_URL = import.meta.env.VITE_API_URL;

export const handle: Handle = async ({ event, resolve }) => {
	let sessionId = event.cookies.get('sessionId');
	if (!sessionId) {
		sessionId = randomBytes(16).toString('hex');
		event.cookies.set('sessionId', sessionId, {
			path: '/',
			httpOnly: true,
			sameSite: 'strict',
			secure: !event.url.hostname.includes('localhost')
		});
	}

	if (!sessionStore.get(sessionId)) {
		sessionStore.create(sessionId, { access_token: null }, 30 * 24 * 60 * 60); // 30 days expiration
	}
	event.locals.session = sessionStore.get(sessionId);
	const response = await resolve(event);
	return response;
};

function initializeServer() {
	client.setConfig({
		baseUrl: VITE_API_URL
	});
	client.interceptors.response.use((response) => {
		if (response.status === 200) {
			console.log(`request to ${response.url} was successful`);
		} else {
			console.error(`request to ${response.url} failed with status ${response.status}`);
		}
		return response;
	});
}

initializeServer();
