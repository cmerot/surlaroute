import { toursGetTourDetails } from '$lib/backend/client/sdk.gen';
import { error } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ params }) => {
	const { data: tour } = await toursGetTourDetails({
		path: {
			id: params.id
		}
	});

	if (!tour) error(404);

	return tour;
};
