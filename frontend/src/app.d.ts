// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
import type { UserPublic } from "$lib/backend/client";

declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			user?: UserPublic;
			authToken?: string;
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}
