import { usersRead } from '$lib/backend/client/services.gen';

export async function load() {
	const { data } = await usersRead();
	return data;
}
