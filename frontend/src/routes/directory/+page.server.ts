import type { DirectoryGetActorsData } from '$lib/backend/client';
import { activitiesReadActivities, directoryGetActors } from '$lib/backend/client';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, cookies }) => {
	const query: DirectoryGetActorsData['query'] = {};

	const limitParam = url.searchParams.get('limit');
	if (limitParam) {
		query.limit = parseInt(limitParam);
	}
	const offsetParam = url.searchParams.get('offset');
	if (offsetParam) {
		query.offset = parseInt(offsetParam);
	}
	const qParam = url.searchParams.get('q');
	if (qParam) {
		query.q = qParam;
	}

	const result = await directoryGetActors({
		query,
		headers: { Authorization: `Bearer ${cookies.get('sessionId')}` }
	});

	if (result.error) {
		// @ts-expect-error: error on the backend, there are multiple types
		const messageActivities = `${result.error.message} ${result.error.detail}`;

		error(result.response.status, messageActivities);
	}

	const resultActivities = await activitiesReadActivities({
		headers: {
			Authorization: `Bearer ${cookies.get('sessionId')}`
		}
	});

	if (resultActivities.error) {
		// @ts-expect-error: error on the backend, there are multiple types
		const messageActivities = `${resultActivities.error.message} ${resultActivities.error.detail}`;

		error(resultActivities.response.status, messageActivities);
	}

	return {
		actorsResult: result.data,
		activitiesResult: resultActivities.data
	};
};
