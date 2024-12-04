import { sessionStore } from '$lib/server/sessionStore';
import { type Actions } from '@sveltejs/kit';
// export function GET({ cookies, event }) {
// 	const session = sessionStore.get(cookies.get('sessionId') || '');
// 	if (session) {
// 		sessionStore.destroy(session.id);
// 	}
// 	cookies.delete('sessionId', { path: '/' });
// 	event.delete('user');
// 	redirect(303, '/');
// }
// import type { Actions } from './$types';

export const actions: Actions = {
	default: async (event) => {
		console.log('logout');

		sessionStore.destroy(event.cookies.get('sessionId') || '');
		event.cookies.delete('sessionId', { path: '/' });
		// redirect(303, '/admin');
	}
};
