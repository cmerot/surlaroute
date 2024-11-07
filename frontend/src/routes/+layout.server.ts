// src/routes/+layout.server.js
export const load = ({ cookies }) => {
	const notification = cookies.get('notification');
	cookies.delete('notification', { path: '/' });
	return { notification: notification };
};
