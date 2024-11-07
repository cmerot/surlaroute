import { z } from 'zod';

export const formSchema = z.object({
	firstName: z.string().min(2),
	lastName: z.string().min(2),
	email: z.string().email(),
	password: z.string().min(8)
});

export type FormSchema = typeof formSchema;
