import { orgsReadOrgs } from '$lib/backend/client/services.gen';
import type { OrgsReadOrgsData } from '$lib/backend/client/types.gen';

export async function load({ url }) {
	const query: OrgsReadOrgsData['query'] = {};

	const limitParam = url.searchParams.get('limit');
	if (limitParam) {
		query.limit = parseInt(limitParam);
	}
	const offsetParam = url.searchParams.get('offset');
	if (offsetParam) {
		query.offset = parseInt(offsetParam);
	}
	const { data, error } = await orgsReadOrgs({ query });

	if (error) {
		return error(500, 'Pas de réponse du serveur');
	}
	return data;
}
