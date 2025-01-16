import type { ErrorResponse, HTTPValidationError } from "./backend/client";

export function getErrorMessage(err: ErrorResponse | HTTPValidationError) {
	let errorMessage: string;
	if (Array.isArray(err.detail)) {
		errorMessage = err.detail.map((e) => e.msg.toString()).join(", ");
	} else {
		errorMessage = err.detail ?? "An error occurred";
	}
	return errorMessage;
}
