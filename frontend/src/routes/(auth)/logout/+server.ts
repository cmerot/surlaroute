import { sessionStore } from '$lib/server/sessionStore.js';
import { redirect } from '@sveltejs/kit';

export function GET({ cookies }) {
	const session = sessionStore.get(cookies.get('sessionId') || '');
	if (session) {
		sessionStore.destroy(session.id);
	}
	cookies.delete('sessionId', { path: '/' });
	redirect(303, '/');
}
