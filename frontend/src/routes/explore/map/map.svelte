<script lang="ts">
	import { cn } from "$lib/utils";
	import type { WithChildren } from "bits-ui";
	import { mode } from "mode-watcher";
	import type { ComponentProps } from "svelte";
	import { MapLibre, type StyleSpecification } from "svelte-maplibre";
	import Controls from "./controls.svelte";
	import { getDefaultStyleName, styles, type Styles } from "./styles";

	type Props = WithChildren<Omit<ComponentProps<typeof MapLibre>, "style">>;

	let {
		map = $bindable(),
		zoom = $bindable(),
		center = $bindable(),
		bounds = $bindable(),
		class: className,
		children,
		...restProps
	}: Props = $props();

	const defaultStyleName = getDefaultStyleName($mode);

	let styleName: keyof Styles = $state(defaultStyleName);
	let style: string | StyleSpecification = $state(styles[defaultStyleName].style);

	$effect(() => {
		style = styles[styleName].style;
	});
</script>

<MapLibre
	class={cn("", className)}
	{style}
	bind:map
	bind:bounds
	bind:zoom
	bind:center
	{...restProps}
	attributionControl={false}
>
	<Controls bind:styleName />
	{@render children?.()}
</MapLibre>
