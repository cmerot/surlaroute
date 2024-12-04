import { client, loginTestToken, usersReadUserMe } from '$lib/backend/client/services.gen';
import type { UserPublic } from '$lib/backend/client/types.gen.js';
import { getApiErrorMessage } from '$lib/backend/utils';
import { sessionStore } from '$lib/server/sessionStore.js';
import { error, redirect } from '@sveltejs/kit';

export async function load({ cookies, url }) {
	console.log('layout.server.load');
	const session = sessionStore.get(cookies.get('sessionId') || '');
	const accessToken = session?.data?.access_token;

	if (!accessToken) {
		redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	client.interceptors.request.use((request) => {
		console.log('add bearer', request.url);
		request.headers.set('Authorization', `Bearer ${accessToken}`);
		return request;
	});

	const { error: err } = await loginTestToken({});
	if (err) {
		redirect(303, `/login?redirectTo=${url.pathname}`);
	}

	const userResult = await usersReadUserMe();
	if (userResult.error) {
		error(userResult.response.status, { message: getApiErrorMessage(userResult.error) });
	}
	return { user: userResult.data as UserPublic };
}
