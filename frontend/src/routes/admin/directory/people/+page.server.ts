// import type { PeopleReadPeopleData } from '$lib/backend/client';
// import { peopleReadPeople } from '$lib/backend/client';
// import { error } from '@sveltejs/kit';

// export async function load({ url }) {
// 	const query: PeopleReadPeopleData['query'] = {};

// 	const limitParam = url.searchParams.get('limit');
// 	if (limitParam) {
// 		query.limit = parseInt(limitParam);
// 	}
// 	const offsetParam = url.searchParams.get('offset');
// 	if (offsetParam) {
// 		query.offset = parseInt(offsetParam);
// 	}
// 	const { data, error: err } = await peopleReadPeople({ query });

// 	if (err) {
// 		return error(500, 'Pas de réponse du serveur');
// 	}
// 	return data;
// }
