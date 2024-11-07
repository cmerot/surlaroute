import { dev } from '$app/environment';
export interface Session {
	id: string;
	data?: SessionData;
	expiresAt: number;
}

export interface SessionData {
	access_token: string | null;
}

class SessionStore {
	private sessions: Map<string, Session> = new Map();

	create(id: string, data: SessionData, expiresIn: number): void {
		const expiresAt = Date.now() + expiresIn * 1000;
		this.sessions.set(id, { id, data, expiresAt });
	}

	get(id: string): Session | undefined {
		const session = this.sessions.get(id);
		if (session && session.expiresAt > Date.now()) {
			return session;
		}
		this.destroy(id);
		return undefined;
	}

	update(id: string, data: SessionData): void {
		const session = this.get(id);
		if (session) {
			session.data = { ...session.data, ...data };
			this.sessions.set(id, session);
		}
	}

	destroy(id: string): void {
		this.sessions.delete(id);
	}

	// Clean up expired sessions periodically
	cleanup(): void {
		for (const [id, session] of this.sessions.entries()) {
			if (session.expiresAt <= Date.now()) {
				this.sessions.delete(id);
			}
		}
	}

	dump(): void {
		this.sessions.entries().forEach(([id, session]) => {
			console.log(id, session);
		});
	}
}

export const sessionStore = new SessionStore();

// Run cleanup every 5 minutes in development, or set up a cron job in production
if (dev) {
	setInterval(() => sessionStore.cleanup(), 5 * 60 * 1000);
}
