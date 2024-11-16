import type { PageServerLoad, Actions } from './$types.js';
import { fail, redirect, error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { formSchema } from './schema.js';
import { usersRegister } from '$lib/backend/client/services.gen.js';
import { getApiErrorMessage } from '$lib/backend/utils.js';
export const load: PageServerLoad = async () => {
	return {
		form: await superValidate(zod(formSchema))
	};
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, {
				form
			});
		}

		const { error: err } = await usersRegister({
			body: {
				full_name: `${form.data.firstName} ${form.data.lastName}`,
				email: form.data.email,
				password: form.data.password
			}
		});

		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		event.cookies.set('notification', 'Your account has been created, you may now log in', {
			path: '/'
		});
		redirect(303, event.url.searchParams.get('redirectTo') ?? '/login');
	}
};
