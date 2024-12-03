import { z } from 'zod';

export const formSchema = z.object({
	email: z.string().email(),
	is_superuser: z.boolean().default(false),
	is_member: z.boolean().default(false),
	is_active: z.boolean().default(false)
});

export type FormSchema = typeof formSchema;
