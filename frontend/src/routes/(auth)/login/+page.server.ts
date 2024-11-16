import type { PageServerLoad, Actions } from './$types.js';
import { fail, redirect, error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { formSchema } from './schema.js';
import { loginLoginAccessToken } from '$lib/backend/client/services.gen.js';
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
			return fail(422, {
				form
			});
		}

		const { data, error: err } = await loginLoginAccessToken({
			body: { username: form.data.email, password: form.data.password }
		});
		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		event.cookies.set('notification', 'Login successful', { path: '/' });
		if (!event.locals.session) {
			return fail(500, { error: 'Session not found' });
		}
		event.locals.session.data = { access_token: data.access_token };
		redirect(303, event.url.searchParams.get('redirectTo') ?? '/');
	}
};
