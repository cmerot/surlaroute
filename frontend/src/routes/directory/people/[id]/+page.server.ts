import { directoryGetPersonDetails } from '$lib/backend/client/sdk.gen';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, cookies }) => {
	const result = await directoryGetPersonDetails({
		path: { id: params.id },
		headers: { Authorization: `Bearer ${cookies.get('sessionId')}` }
	});

	if (result.error) {
		// @ts-expect-error: error on the backend, there are multiple types
		const message = `${result.error.message} ${result.error.detail}`;

		error(result.response.status, message);
	}

	return result.data;
};
