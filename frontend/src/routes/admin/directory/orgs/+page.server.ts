import { orgsReadOrgs } from '$lib/backend/client/services.gen';

export async function load() {
	const { data } = await orgsReadOrgs();
	return data;
}
