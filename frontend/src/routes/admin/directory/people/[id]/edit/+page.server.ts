// import {
// 	peopleDeletePerson,
// 	peopleReadPersonById,
// 	peopleUpdatePerson
// } from '$lib/backend/client/sdk.gen';
// import { getApiErrorMessage } from '$lib/backend/utils.js';
// import { error, fail, redirect } from '@sveltejs/kit';
// import { message, superValidate } from 'sveltekit-superforms';
// import { zod } from 'sveltekit-superforms/adapters';
// import type { Actions, PageServerLoad } from './$types.js';
// import { formSchema } from './schema';

// export const load: PageServerLoad = async ({ params }) => {
// 	const { data: person } = await peopleReadPersonById({
// 		path: {
// 			id: params.id
// 		}
// 	});

// 	if (!person) error(404);

// 	const form = await superValidate(person, zod(formSchema));

// 	return { form };
// };

// export const actions: Actions = {
// 	update: async (event) => {
// 		const form = await superValidate(event, zod(formSchema));

// 		if (!form.valid) {
// 			return fail(400, { form });
// 		}

// 		const { error: err } = await peopleUpdatePerson({
// 			body: form.data,
// 			path: {
// 				id: event.params.id
// 			}
// 		});

// 		if (err) {
// 			error(422, { message: getApiErrorMessage(err) });
// 		}

// 		return message(form, 'Person updated');
// 	},
// 	delete: async (event) => {
// 		const { error: err } = await peopleDeletePerson({
// 			path: {
// 				id: event.params.id
// 			}
// 		});
// 		if (err) {
// 			error(422, { message: getApiErrorMessage(err) });
// 		}

// 		event.cookies.set('notification', 'Person deleted', {
// 			path: '/'
// 		});
// 		redirect(303, '/admin/directory/people');
// 	}
// };
