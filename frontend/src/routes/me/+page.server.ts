import { directoryGetPerson } from "$lib/backend/client";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { getErrorMessage } from "$lib/slr-utils";

export const load: PageServerLoad = async ({ cookies, locals }) => {
	const user = locals.user;
	console.log(locals);
	if (!user) {
		error(403, "Vous n'êtes pas connecté");
	}
	if (!user.person) {
		return { user, person: undefined };
	}

	const result = await directoryGetPerson({
		path: { id: user.person.id },
		headers: {
			Authorization: `Bearer ${cookies.get("sessionId")}`,
		},
	});

	if (result.error) {
		error(404, getErrorMessage(result.error));
	}

	return { person: result.data, user };
};
