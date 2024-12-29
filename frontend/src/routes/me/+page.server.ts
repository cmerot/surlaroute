// import { directoryGetPersonDetails, type DirectoryGetPersonDetailsData, type PersonFull_Explore } from '$lib/backend/client';
// import { error } from '@sveltejs/kit';

// export async function load({ locals }) {
// 	const user = locals.session?.data?.user;
// 	if (!user) {
// 		error(404, 'User not found');
// 	}
// 	return { user };
// }
import { directoryGetPersonDetails } from '$lib/backend/client';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, locals }) => {
	const user = locals.session?.data?.user;
	if (!user) {
		error(403, "Vous n'êtes pas connecté");
	}
	if (!user.person) {
		return { user, person: undefined };
	}

	const result = await directoryGetPersonDetails({
		path: { id: user.person.id },
		headers: { Authorization: `Bearer ${cookies.get('sessionId')}` }
	});

	if (result.error) {
		console.log(result.error);
		error(404, 'Not found');
	}

	return { person: result.data, user };
};
