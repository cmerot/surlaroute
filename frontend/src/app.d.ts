// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
import type { UserPublic } from '$lib/backend/client';
import type { Session } from '$lib/server/sessionStore';

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
