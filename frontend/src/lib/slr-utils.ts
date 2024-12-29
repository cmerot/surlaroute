import { getContext } from 'svelte';

export type CrumbsData = {
	[key: string]: string;
};

export const addCrumb = (url: string, title: string) => {
	const data: CrumbsData = getContext('crumbs-data');
	data[url] = title;
	console.log('addCrumb', data);
};
