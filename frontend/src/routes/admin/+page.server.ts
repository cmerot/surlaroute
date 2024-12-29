// import type { UsersReadData } from '$lib/backend/client';
// import { usersRead } from '$lib/backend/client';
// import { error } from '@sveltejs/kit';

// export async function load({ url, locals }) {
// 	// const query: UsersReadData['query'] = {};

// 	// const limitParam = url.searchParams.get('limit');
// 	// if (limitParam) {
// 	// 	query.limit = parseInt(limitParam);
// 	// }
// 	// const offsetParam = url.searchParams.get('offset');
// 	// if (offsetParam) {
// 	// 	query.offset = parseInt(offsetParam);
// 	// }
// 	// const result = await usersRead({ query });

// 	// if (result.error) {
// 	// 	// @ts-expect-error: result.error.detail is a string
// 	// 	error(result.response.status, { message: result.error.detail });
// 	// }
// 	// return result.data;
// }
