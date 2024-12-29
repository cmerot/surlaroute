import type { ToursGetToursData } from '$lib/backend/client';
import { toursGetTours } from '$lib/backend/client';
import { error } from '@sveltejs/kit';

export async function load({ url, cookies }) {
	const query: ToursGetToursData['query'] = {};

	const limitParam = url.searchParams.get('limit');
	if (limitParam) {
		query.limit = parseInt(limitParam);
	}
	const offsetParam = url.searchParams.get('offset');
	if (offsetParam) {
		query.offset = parseInt(offsetParam);
	}
	const result = await toursGetTours({
		query,
		headers: { Authorization: `Bearer ${cookies.get('sessionId')}` }
	});
	if (result.error) {
		// @ts-expect-error: result.error.detail is a string
		error(result.response.status, { message: result.error });
	}

	return result.data;
}
