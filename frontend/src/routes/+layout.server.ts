import type { LayoutServerLoad } from './$types';
export const load: LayoutServerLoad = async ({ cookies }) => {
	const notification = cookies.get('notification');
	cookies.delete('notification', { path: '/' });

	return { notification };
};
