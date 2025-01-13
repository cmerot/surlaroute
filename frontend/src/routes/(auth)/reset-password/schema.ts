import { z } from "zod";

export const formSchema = z
	.object({
		newPassword: z.string().min(8),
		confirmPassword: z.string().min(8),
	})
	.superRefine(({ newPassword, confirmPassword }, ctx) => {
		if (newPassword !== confirmPassword) {
			ctx.addIssue({
				code: "custom",
				message: "Les mots de passe ne correspondent pas",
				path: ["confirmPassword"],
			});
		}
	});

export type FormSchema = typeof formSchema;
