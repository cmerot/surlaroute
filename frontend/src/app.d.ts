// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
import type { Session } from '$lib/server/sessionStore';
import type { UserPublic } from '$lib/backend/client/types.gen.js';

declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			session?: Session;
			user?: UserPublic;
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
