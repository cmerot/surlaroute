import type { ToursGetToursData } from '$lib/backend/client';
import { toursGetTours } from '$lib/backend/client';
import { error } from '@sveltejs/kit';

export async function load({ url }) {
	const query: ToursGetToursData['query'] = {};

	const limitParam = url.searchParams.get('limit');
	if (limitParam) {
		query.limit = parseInt(limitParam);
	}
	const offsetParam = url.searchParams.get('offset');
	if (offsetParam) {
		query.offset = parseInt(offsetParam);
	}
	const { data, error: err } = await toursGetTours({ query });

	if (err) {
		return error(500, 'Pas de réponse du serveur');
	}
	return data;
}
