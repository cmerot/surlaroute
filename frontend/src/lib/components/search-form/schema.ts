import { z } from 'zod';

export const formSchema = z.object({
	q: z.string()
});

export type FormSchema = typeof formSchema;
