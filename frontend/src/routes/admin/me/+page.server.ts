import { usersReadMe } from '$lib/backend/client/services.gen';

export async function load() {
	const { data } = await usersReadMe();
	return data;
}
