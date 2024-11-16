import { directoryCreatePerson } from '$lib/backend/client/services.gen.js';
import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions, PageServerLoad } from './$types.js';
import { formSchema } from './schema';
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
		const { error: err, data: person } = await directoryCreatePerson({
			body: form.data
		});
		if (err) {
			error(422, { message: getApiErrorMessage(err) });
		}

		event.cookies.set('notification', 'Person created', {
			path: '/'
		});
		redirect(303, `/admin/directory/people/${person.id}`);
	}
};
