import { usersRegister } from "$lib/backend/client/sdk.gen";
import { getApiErrorMessage } from "$lib/backend/utils.js";
import { error, fail, redirect } from "@sveltejs/kit";
import { superValidate } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";
import type { Actions, PageServerLoad } from "./$types.js";
import { formSchema } from "./schema.js";
export const load: PageServerLoad = async () => {
	return {
		form: await superValidate(zod(formSchema)),
	};
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, {
				form,
			});
		}

		const { error: err } = await usersRegister({
			body: {
				email: form.data.email,
				password: form.data.password,
			},
		});

		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		event.cookies.set("notification", "Votre compte a été créé et sera bientôt validé", {
			path: "/",
		});
		redirect(303, event.url.searchParams.get("redirectTo") ?? "/login");
	},
};
