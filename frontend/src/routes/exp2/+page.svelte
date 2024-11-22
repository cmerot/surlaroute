<script>
	import { onMount } from 'svelte';
	let input,
		results,
		focused = false,
		query = '';
	let resultsVisible = false;

	const showResults = () => (resultsVisible = true);
	const hideResults = () => (resultsVisible = false);

	onMount(() => {
		const onEscape = (event) => {
			if (event.key === 'Escape') {
				hideResults();
				input.focus();
			}
		};

		document.addEventListener('keydown', onEscape);
		return () => {
			document.removeEventListener('keydown', onEscape);
		};
	});
</script>

<div>
	<input
		bind:this={input}
		type="text"
		placeholder="Search..."
		on:focus={() => showResults()}
		on:input={() => showResults()}
	/>
	<div
		bind:this={results}
		class="results {resultsVisible ? 'visible' : ''}"
		on:mouseenter={() => (focused = true)}
		on:mouseleave={() => (focused = false)}
	>
		<!-- Render search results here -->
	</div>
</div>

<input
	type="text"
	bind:this={input}
	on:focus={() => results.classList.add('visible')}
	on:blur={() => {
		if (!focused) results.classList.remove('visible');
	}}
	on:keydown={(e) => {
		if (e.key === 'Escape') {
			results.classList.remove('visible');
		}
	}}
	bind:value={query}
/>

<div
	bind:this={results}
	class:visible={query.length > 0}
	on:mouseenter={() => (focused = true)}
	on:mouseleave={() => (focused = false)}
>
	{#if query.length > 0}
		<p>Search results for "{query}"</p>
	{/if}
</div>

<style>
	.results {
		display: none;
	}
	.results.visible {
		display: block;
	}
</style>
