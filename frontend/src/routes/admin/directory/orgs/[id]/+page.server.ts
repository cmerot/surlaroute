import { orgsReadOrgById } from '$lib/backend/client/services.gen.js';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types.js';

export const load: PageServerLoad = async ({ params }) => {
	const { data: org } = await orgsReadOrgById({
		path: {
			id: params.id
		}
	});
	if (!org) return error(404);
	return org;
};
