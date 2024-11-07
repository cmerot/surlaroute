import type { PageServerLoad, Actions } from './$types.js';
import { fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { formSchema } from './schema.js';
import { loginRecoverPassword } from '$lib/backend/client';
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

		const { error: err } = await loginRecoverPassword({
			path: { email: form.data.email }
		});

		if (err) {
			console.error(getApiErrorMessage(err));
		}
		event.cookies.set(
			'notification',
			'If your email exists, you will receive an email with further instructions.',
			{
				path: '/'
			}
		);
		redirect(303, event.url.searchParams.get('redirectTo') ?? '/');
	}
};
