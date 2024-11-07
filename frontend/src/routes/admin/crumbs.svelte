<script lang="ts">
	import { getContext } from 'svelte';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb';
	import { page } from '$app/stores';

	const data: { [key: string]: string } = getContext('crumbs-data');

	let crumbs: { title: string; url: string }[] = $derived.by(() => {
		console.log('derived by', data);
		const tokens = $page.url.pathname.split('/').filter((t) => t !== '');
		let tokenPath = '';
		return tokens
			.map((t) => {
				tokenPath += '/' + t;
				t = data[tokenPath];
				return { title: t, url: tokenPath };
			})
			.filter((t) => t.title);
	});
</script>

<Breadcrumb.Root>
	<Breadcrumb.List>
		{#each crumbs as item, index}
			<Breadcrumb.Item>
				<Breadcrumb.Link href={item.url}>{item.title}</Breadcrumb.Link>
			</Breadcrumb.Item>
			{#if index < crumbs.length - 1}
				<Breadcrumb.Separator />
			{/if}
		{/each}
	</Breadcrumb.List>
</Breadcrumb.Root>
