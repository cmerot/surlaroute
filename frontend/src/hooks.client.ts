import { client } from '$lib/backend/client';
import type { ClientInit } from '@sveltejs/kit';

const VITE_API_URL = import.meta.env.VITE_API_URL;

export const init: ClientInit = async () => {
	client.setConfig({
		baseUrl: VITE_API_URL
	});
};
