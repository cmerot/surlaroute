<script module lang="ts">
</script>

<script lang="ts" generics="T extends {id: string; name: string}">
	import type { HTTPValidationError } from '$lib/backend/client';
	import { buttonVariants } from '$lib/components/ui/button';
	import * as Command from '$lib/components/ui/command';
	import * as Popover from '$lib/components/ui/popover';
	import type { Options, RequestResult } from '@hey-api/client-fetch';
	import { tick } from 'svelte';

	type Props = {
		renderItem: RenderItem<T>;
		onValueChange: OnValueChange<T | undefined>;
		read: Read;
		title: string;
	};

	interface RenderItem<T> {
		(item: T): string;
	}

	interface OnValueChange<T> {
		(item: T): void;
	}

	type ReadData = {
		query: {
			limit: number;
			q: string;
		};
	};

	type ReadResponse = {
		total: number;
		limit: number;
		offset: number;
		results: Array<T>;
	};

	type Read = <ThrowOnError extends boolean = false>(
		options: Options<ReadData, ThrowOnError>
	) => RequestResult<ReadResponse, HTTPValidationError, ThrowOnError>;

	let { renderItem, onValueChange, read, title }: Props = $props();

	let q = $state('');
	let value: T | undefined = $state();
	let results: ReadResponse['results'] = $state([]);
	let triggerRef = $state<HTMLButtonElement>(null!);
	let open = $state(false);

	async function updateResults(q: string) {
		if (q.length < 1) {
			results = [];
			value = undefined;
			return;
		}
		const { data, error } = await read({ query: { q, limit: 10 } });
		if (error) {
			console.error(error);
			return;
		}
		if (data?.results) {
			results = data.results;
		}
	}

	$effect(() => {
		updateResults(q);
	});

	$effect(() => {
		console.log('yo');
		onValueChange(value);
	});

	function handleSelect(v: T) {
		value = v;
		open = false;
		tick().then(() => {
			triggerRef.focus();
		});
	}
</script>

<Popover.Root bind:open>
	<Popover.Trigger class={buttonVariants({ variant: 'outline' })} bind:ref={triggerRef}>
		{value ? renderItem(value) : title}
	</Popover.Trigger>
	<Popover.Content class="">
		<div class="">
			<Command.Root shouldFilter={false}>
				<Command.Input placeholder="Nom du lieu" bind:value={q} {onfocus} {onblur} />
				<Command.List>
					{#if results.length > 0}
						{#each results as item}
							<Command.Item onSelect={() => handleSelect(item)}>
								{renderItem(item)}
							</Command.Item>
						{/each}
					{:else if q.length > 0}
						<Command.Empty forceMount>No results found.</Command.Empty>
					{:else}
						<Command.Empty forceMount>Start typing to search.</Command.Empty>
					{/if}
				</Command.List>
			</Command.Root>
		</div>
	</Popover.Content>
</Popover.Root>
