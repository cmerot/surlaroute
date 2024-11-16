import { peopleReadPeople } from '$lib/backend/client/services.gen';

export async function load() {
	const { data } = await peopleReadPeople();
	return data;
}
