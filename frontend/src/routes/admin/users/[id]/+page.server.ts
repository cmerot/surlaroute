import {
	usersDeleteUser,
	usersReadUserById,
	usersUpdateUser
} from '$lib/backend/client/services.gen.js';
import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions, PageServerLoad } from './$types.js';
import { formSchema } from './schema';
import { getApiErrorMessage } from '$lib/backend/utils.js';

export const load: PageServerLoad = async ({ params }) => {
	const { data: user } = await usersReadUserById({
		path: {
			user_id: params.id
		}
	});
	if (!user) error(404);

	return {
		form: await superValidate(
			{
				...user,
				full_name: user.full_name ?? ''
			},
			zod(formSchema)
		)
	};
};

export const actions: Actions = {
	update: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, {
				form
			});
		}
		const { error: err } = await usersUpdateUser({
			body: form.data,
			path: {
				user_id: event.params.id
			}
		});

		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		event.cookies.set('notification', 'User updated', {
			path: '/'
		});
	},
	delete: async (event) => {
		const { error: err } = await usersDeleteUser({
			path: {
				user_id: event.params.id
			}
		});
		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		event.cookies.set('notification', 'User deleted', {
			path: '/'
		});
		redirect(303, '/admin/users');
	}
};