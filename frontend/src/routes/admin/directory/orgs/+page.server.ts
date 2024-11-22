import { organisationsReadOrganisations } from '$lib/backend/client/services.gen';

export async function load() {
	const { data } = await organisationsReadOrganisations();
	return data;
}
