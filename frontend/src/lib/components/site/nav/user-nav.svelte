<script lang="ts">
	import { enhance } from "$app/forms";
	import { Theme } from "$lib/components/icons";
	import { buttonVariants } from "$lib/components/ui/button/index.js";
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import { auth } from "$lib/stores/auth";
	import { cn } from "$lib/utils";
	import { CircleUser, LogIn, LogOut, MonitorCog, Moon, Palette, Sun } from "lucide-svelte";
	import { mode, setMode, setTheme, theme } from "mode-watcher";

	const user = $derived($auth.user);

	let modeValue = $state($mode || "light");
	let themeValue: string = $state($theme || "nb");

	$effect(() => {
		setTheme(themeValue);
	});
	$effect(() => {
		setMode(modeValue);
	});
</script>

<nav class="flex flex-1 items-center justify-end">
	<DropdownMenu.Root>
		<DropdownMenu.Trigger
			class={cn(
				buttonVariants({
					variant: "ghost",
					class:
						"mr-2 px-0 text-base hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 [&_svg]:size-6",
				}),
			)}
		>
			<CircleUser />
		</DropdownMenu.Trigger>
		<DropdownMenu.Content align="end" class="relative z-[40] flex items-center gap-2 ">
			<DropdownMenu.Group>
				{#if user}
					<DropdownMenu.GroupHeading class="px-5 py-3 text-xs font-normal text-muted-foreground">
						{user.email}
					</DropdownMenu.GroupHeading>
					<DropdownMenu.Item class="px-5 py-3">
						{#snippet child({ props })}
							<a href="/me" {...props}>
								<CircleUser class="mr-2 size-4" />
								<span>Mon compte</span>
							</a>
						{/snippet}
					</DropdownMenu.Item>
					<DropdownMenu.Item class="px-5 py-3">
						{#snippet child({ props })}
							<form action="/logout" method="post" use:enhance {...props}>
								<LogOut class="mr-2 size-4" />
								<button type="submit" class="flex w-full"> Déconnexion </button>
							</form>
						{/snippet}
					</DropdownMenu.Item>
				{:else}
					<DropdownMenu.Item class="px-5 py-3">
						{#snippet child({ props })}
							<a href="/login" {...props}>
								<LogIn class="mr-2 size-4" />
								Connexion
							</a>
						{/snippet}
					</DropdownMenu.Item>
				{/if}
				<DropdownMenu.Separator />
				<DropdownMenu.Group>
					<DropdownMenu.GroupHeading class="px-5 py-3 text-xs font-normal text-muted-foreground">
						Appararence
					</DropdownMenu.GroupHeading>

					<DropdownMenu.Sub>
						<DropdownMenu.SubTrigger class="px-5 py-3">
							{#if $mode === "light"}
								<Sun />
								<span> Mode clair </span>
							{:else if $mode === "dark"}
								<Moon />
								<span> Mode sombre </span>
							{:else}
								<MonitorCog />
								<span> Mode du système </span>
							{/if}
						</DropdownMenu.SubTrigger>
						<DropdownMenu.SubContent>
							<DropdownMenu.RadioGroup bind:value={modeValue}>
								<DropdownMenu.GroupHeading class="py-3 text-xs font-normal text-muted-foreground">
									Mode
								</DropdownMenu.GroupHeading>
								<DropdownMenu.RadioItem value="light" class="py-3 pr-5">
									<Sun class="mr-2 size-4" />
									<span>Mode clair</span>
								</DropdownMenu.RadioItem>
								<DropdownMenu.RadioItem value="dark" class="py-3 pr-5">
									<Moon class="mr-2 size-4" />
									<span>Mode sombre</span>
								</DropdownMenu.RadioItem>
								<DropdownMenu.RadioItem value="system" class="py-3 pr-5">
									<MonitorCog class="mr-2 size-4" />
									<span>Mode du système</span>
								</DropdownMenu.RadioItem>
							</DropdownMenu.RadioGroup>
						</DropdownMenu.SubContent>
					</DropdownMenu.Sub>
					<DropdownMenu.Sub>
						<DropdownMenu.SubTrigger class="px-5 py-3">
							<Palette />
							<span> Thème {$theme} </span>
						</DropdownMenu.SubTrigger>
						<DropdownMenu.SubContent>
							<DropdownMenu.RadioGroup bind:value={themeValue}>
								<DropdownMenu.GroupHeading class="py-3 text-xs font-normal text-muted-foreground">
									Thème
								</DropdownMenu.GroupHeading>
								<DropdownMenu.RadioItem value="nb" class="py-3 pr-5">
									<Theme theme="nb" class="mr-2 size-4" />
									<span>Thème N & B</span>
								</DropdownMenu.RadioItem>
								<DropdownMenu.RadioItem value="vert" class="py-3 pr-5">
									<Theme theme="vert" class="mr-2 size-4" />
									<span>Thème vert</span>
								</DropdownMenu.RadioItem>
								<DropdownMenu.RadioItem value="marron" class="py-3 pr-5">
									<Theme theme="marron" class="mr-2 size-4" />
									<span>Thème marron</span>
								</DropdownMenu.RadioItem>
							</DropdownMenu.RadioGroup>
						</DropdownMenu.SubContent>
					</DropdownMenu.Sub>
				</DropdownMenu.Group>
			</DropdownMenu.Group>
		</DropdownMenu.Content>
	</DropdownMenu.Root>
</nav>
