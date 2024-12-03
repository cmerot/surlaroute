import { peopleReadPersonById } from '$lib/backend/client/services.gen.js';
import { error } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ params }) => {
	const { data: person } = await peopleReadPersonById({
		path: {
			id: params.id
		}
	});

	if (!person) error(404);

	return person;
};
