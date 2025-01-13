import { toursGetAllTours } from "$lib/backend/client";
import { getErrorMessage } from "$lib/slr-utils";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ url, locals }) => {
	const q = url.searchParams.get("q") ?? "";
	const limit = Number(url.searchParams.get("limit")) || 10;
	const offset = Number(url.searchParams.get("offset")) || 0;

	const result = await toursGetAllTours({
		headers: {
			Authorization: `Bearer ${locals.authToken}`,
		},
		query: { limit, offset, q },
	});

	if (result.error) {
		error(result.response.status, getErrorMessage(result.error));
	}

	return {
		results: result.data.results,
		total: result.data.total,
		query: { limit, offset, q },
	};
};
