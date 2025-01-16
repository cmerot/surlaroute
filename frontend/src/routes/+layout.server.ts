import type { ServerLoadEvent } from '@sveltejs/kit';

export function load({ locals }: ServerLoadEvent) {
	return {
		authToken: locals.authToken,
		user: locals.user
	};
}
