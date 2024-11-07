import type { HTTPValidationError } from './client';

export const getApiErrorMessage = (err: HTTPValidationError) => {
	let message;
	if (typeof err.detail === 'string') {
		message = err.detail;
	} else if (Array.isArray(err.detail)) {
		message = err.detail[0].msg;
	} else {
		message = 'Something went wrong';
	}
	return message;
};
