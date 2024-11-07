import { z } from 'zod';

export const formSchema = z.object({
	full_name: z.string().min(3),
	email: z.string().email(),
	is_superuser: z.boolean().default(false),
	is_active: z.boolean().default(true)
});

export type FormSchema = typeof formSchema;
