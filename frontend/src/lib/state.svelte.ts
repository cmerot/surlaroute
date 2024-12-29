import type { UserPublic } from '$lib/backend/client';

export const myGlobalState: { user?: UserPublic } = $state({});
