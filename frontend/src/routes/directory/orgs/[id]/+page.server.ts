import { directoryGetOrg } from '$lib/backend/client/sdk.gen';
import { getErrorMessage } from '$lib/slr-utils';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
	const result = await directoryGetOrg({
		path: { id: params.id },
		headers: {
			Authorization: `Bearer ${locals.authToken}`
		}
	});

	if (result.error) {
		error(result.response.status, getErrorMessage(result.error));
	}
	return { org: result.data };
};
