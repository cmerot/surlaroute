export async function load({ locals }) {
	return { user: locals.session?.data?.user };
}
