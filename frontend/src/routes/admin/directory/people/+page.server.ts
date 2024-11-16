import { directoryReadPeople } from '$lib/backend/client/services.gen';

export async function load() {
	const { data } = await directoryReadPeople();
	return data;
}
