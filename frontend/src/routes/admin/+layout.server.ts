import { client, loginTestToken, usersReadUserMe } from '$lib/backend/client';
import type { UserPublic } from '$lib/backend/client/sdk.gen';
import { getApiErrorMessage } from '$lib/backend/utils';
import { sessionStore } from '$lib/server/sessionStore.js';
import { error, redirect } from '@sveltejs/kit';

export async function load({ cookies, url }) {
	const session = sessionStore.get(cookies.get('sessionId') || '');
	const accessToken = session?.data?.access_token;

	if (!accessToken) {
		redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	const { error: err } = await loginTestToken({});
	if (err) {
		redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	const userResult = await usersReadUserMe();
	if (userResult.error) {
		error(userResult.response.status, { message: getApiErrorMessage(userResult.error) });
	}

	if (userResult.data) {
		if (!userResult.data.is_superuser) {
			error(403, 'not enough privileges');
		}
		return { user: userResult.data as UserPublic };
	} else {
		error(500, 'should not be here');
	}
}
