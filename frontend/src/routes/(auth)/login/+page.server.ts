import { loginAccessToken, usersReadUserMe } from '$lib/backend/client/sdk.gen';
import { getApiErrorMessage } from '$lib/backend/utils.js';
import { sessionStore } from '$lib/server/sessionStore.js';
import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions, PageServerLoad } from './$types.js';
import { formSchema } from './schema.js';

export const load: PageServerLoad = async () => {
	return {
		form: await superValidate(zod(formSchema))
	};
};

export const actions: Actions = {
	default: async (event) => {
		// Validate the form
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(422, {
				form
			});
		}

		// Get access token
		const result = await loginAccessToken({
			body: {
				username: form.data.email,
				password: form.data.password
			}
		});
		if (result.error) {
			error(result.response.status, {
				message: getApiErrorMessage(result.error)
			});
		}

		// Get the user
		const userResult = await usersReadUserMe({
			headers: {
				Authorization: `Bearer ${result.data.access_token}`
			}
		});

		if (userResult.error) {
			error(userResult.response.status);
		}

		// Save the session
		const sessionId = result.data.access_token;
		sessionStore.getOrCreate(
			sessionId,
			{ authToken: sessionId, user: userResult.data },
			30 * 24 * 60 * 60
		);

		// Save sessionId in a cookie
		event.cookies.set('sessionId', sessionId, {
			path: '/',
			httpOnly: true,
			sameSite: 'strict',
			secure: !event.url.hostname.includes('localhost')
		});

		redirect(303, event.url.searchParams.get('redirectTo') ?? '/');
	}
};
