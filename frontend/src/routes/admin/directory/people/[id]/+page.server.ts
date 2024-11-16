import {
	directoryDeletePerson,
	directoryReadPersonById,
	directoryUpdatePerson
} from '$lib/backend/client/services.gen.js';
import { message } from 'sveltekit-superforms';
import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions, PageServerLoad } from './$types.js';
import { formSchema } from './schema';
import { getApiErrorMessage } from '$lib/backend/utils.js';

export const load: PageServerLoad = async ({ params }) => {
	const { data: person } = await directoryReadPersonById({
		path: {
			id: params.id
		}
	});

	if (!person) error(404);

	const form = await superValidate(person, zod(formSchema));

	return { form };
};

export const actions: Actions = {
	update: async (event) => {
		const form = await superValidate(event, zod(formSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		const { error: err } = await directoryUpdatePerson({
			body: form.data,
			path: {
				id: event.params.id
			}
		});

		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		return message(form, 'Person updated');
	},
	delete: async (event) => {
		const { error: err } = await directoryDeletePerson({
			path: {
				id: event.params.id
			}
		});
		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		event.cookies.set('notification', 'Person deleted', {
			path: '/'
		});
		redirect(303, '/admin/directory/people');
	}
};
