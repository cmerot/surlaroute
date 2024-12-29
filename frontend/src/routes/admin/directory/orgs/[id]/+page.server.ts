// import { directoryGetOrgDetails } from '$lib/backend/client/sdk.gen';
// import { error } from '@sveltejs/kit';
// import type { PageServerLoad } from './$types.js';

// export const load: PageServerLoad = async ({ params }) => {
// 	const { data: org } = await directoryGetOrgDetails({
// 		path: {
// 			id: params.id
// 		}
// 	});
// 	if (!org) error(404);
// 	return org;
// };
