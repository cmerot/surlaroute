import { usersReadUsers } from '$lib/backend/client/services.gen';

export async function load() {
	const { data } = await usersReadUsers();
	return data;
}
