import type { PageLoad } from "./$types";
export const ssr = false;

export const load: PageLoad = ({ data }) => {
	return data;
};
