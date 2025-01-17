import type { ErrorResponse, HttpValidationError } from "$lib/backend/client";

export function getErrorMessage(err: ErrorResponse | HttpValidationError) {
	let errorMessage: string;
	if (Array.isArray(err.detail)) {
		errorMessage = err.detail.map((e) => e.msg.toString()).join(", ");
	} else {
		errorMessage = err.detail ?? "An error occurred";
	}
	return errorMessage;
}

export function getCookie(name: string) {
	// Add semicolon to handle edge case of last cookie
	const cookies = document.cookie + ";";
	const pattern = new RegExp(`${name}=([^;]*);`);
	const match = cookies.match(pattern);
	return match ? decodeURIComponent(match[1]) : null;
}
