import { z } from 'zod';

export const formSchema = z.object({
	name: z.string().min(3).max(40)
	// email: z.string().email()
});

export type FormSchema = typeof formSchema;
