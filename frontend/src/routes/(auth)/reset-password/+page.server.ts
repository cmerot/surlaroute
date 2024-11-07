import type { PageServerLoad, Actions } from './$types.js';
import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { formSchema } from './schema.js';
import { loginResetPassword } from '$lib/backend/client/services.gen.js';
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

		const token = event.url.searchParams.get('token');
		if (!token) {
			error(500, 'Auth token invalid');
		}
		const { error: err } = await loginResetPassword({
			body: { token, new_password: form.data.newPassword }
		});

		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		event.cookies.set('notification', 'Password changed', { path: '/' });
		redirect(303, event.url.searchParams.get('redirectTo') ?? '/login');
	}
};
