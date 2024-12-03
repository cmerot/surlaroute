import { usersRead } from '$lib/backend/client/services.gen';
import type { UsersReadData } from '$lib/backend/client/types.gen';

export async function load({ url }) {
	const query: UsersReadData['query'] = {};

	const limitParam = url.searchParams.get('limit');
	if (limitParam) {
		query.limit = parseInt(limitParam);
	}
	const offsetParam = url.searchParams.get('offset');
	if (offsetParam) {
		query.offset = parseInt(offsetParam);
	}
	const { data, error } = await usersRead({ query });

	if (error) {
		return error(500, 'Pas de réponse du serveur');
	}
	return data;
}
