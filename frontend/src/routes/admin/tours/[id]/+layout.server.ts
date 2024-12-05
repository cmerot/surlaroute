import { toursReadTourById } from '$lib/backend/client/services.gen.js';
import { error } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ params }) => {
	const { data: tour } = await toursReadTourById({
		path: {
			id: params.id
		}
	});

	if (!tour) error(404);

	return tour;
};
