import { sessionStore } from '$lib/server/sessionStore.js';
import type { Actions } from './$types.js';
import { redirect } from '@sveltejs/kit';

export const actions: Actions = {
	default: async ({ locals, cookies }) => {
		const sessionId = cookies.get('sessionId');

		if (sessionId) {
			sessionStore.destroy(sessionId);
			cookies.delete('sessionId', { path: '/' });
			delete locals.session;
		}

		redirect(303, '/');
	}
};
