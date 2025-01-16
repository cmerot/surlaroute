<script lang="ts">
	import type { ContactPublic } from "$lib/backend/client";
	import { cn } from "$lib/utils.js";
	import type { SvelteHTMLElements } from "svelte/elements";
	import { Address, EmailAddress, PhoneNumber, Website } from "../../icons";

	type ContactResultProps = SvelteHTMLElements["span"] & {
		contact?: ContactPublic | null;
	};

	const { class: className, contact, ...restProps }: ContactResultProps = $props();
</script>

<span class={cn("flex gap-4", className)} {...restProps}>
	<Address class="size-5 {!contact?.address?.q ? 'text-muted-foreground/50' : ''}" />
	<PhoneNumber class="size-5 {!contact?.phone_number ? 'text-muted-foreground/50' : ''}" />
	<EmailAddress class="size-5 {!contact?.email_address ? 'text-muted-foreground/50' : ''}" />
	<Website class="size-5 {!contact?.website ? 'text-muted-foreground/50' : ''}" />
</span>
