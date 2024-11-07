import { usersReadUserMe } from '$lib/backend/client/services.gen';

export async function load() {
	const { data } = await usersReadUserMe();
	return data;
}
