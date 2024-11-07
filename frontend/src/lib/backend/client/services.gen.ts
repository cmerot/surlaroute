// This file is auto-generated by @hey-api/openapi-ts

import {
	createClient,
	createConfig,
	type Options,
	urlSearchParamsBodySerializer
} from '@hey-api/client-fetch';
import type {
	LoginLoginAccessTokenData,
	LoginLoginAccessTokenError,
	LoginLoginAccessTokenResponse,
	LoginTestTokenError,
	LoginTestTokenResponse,
	LoginRecoverPasswordData,
	LoginRecoverPasswordError,
	LoginRecoverPasswordResponse,
	LoginResetPasswordData,
	LoginResetPasswordError,
	LoginResetPasswordResponse,
	LoginRecoverPasswordHtmlContentData,
	LoginRecoverPasswordHtmlContentError,
	LoginRecoverPasswordHtmlContentResponse,
	UsersReadUsersData,
	UsersReadUsersError,
	UsersReadUsersResponse,
	UsersCreateUserData,
	UsersCreateUserError,
	UsersCreateUserResponse,
	UsersReadUserMeError,
	UsersReadUserMeResponse,
	UsersDeleteUserMeError,
	UsersDeleteUserMeResponse,
	UsersUpdateUserMeData,
	UsersUpdateUserMeError,
	UsersUpdateUserMeResponse,
	UsersUpdatePasswordMeData,
	UsersUpdatePasswordMeError,
	UsersUpdatePasswordMeResponse,
	UsersRegisterUserData,
	UsersRegisterUserError,
	UsersRegisterUserResponse,
	UsersReadUserByIdData,
	UsersReadUserByIdError,
	UsersReadUserByIdResponse,
	UsersUpdateUserData,
	UsersUpdateUserError,
	UsersUpdateUserResponse,
	UsersDeleteUserData,
	UsersDeleteUserError,
	UsersDeleteUserResponse,
	UtilsTestEmailData,
	UtilsTestEmailError,
	UtilsTestEmailResponse,
	UtilsHealthCheckError,
	UtilsHealthCheckResponse,
	ItemsReadItemsData,
	ItemsReadItemsError,
	ItemsReadItemsResponse,
	ItemsCreateItemData,
	ItemsCreateItemError,
	ItemsCreateItemResponse,
	ItemsReadItemData,
	ItemsReadItemError,
	ItemsReadItemResponse,
	ItemsUpdateItemData,
	ItemsUpdateItemError,
	ItemsUpdateItemResponse,
	ItemsDeleteItemData,
	ItemsDeleteItemError,
	ItemsDeleteItemResponse
} from './types.gen';

export const client = createClient(createConfig());

/**
 * Login Access Token
 * OAuth2 compatible token login, get an access token for future requests
 */
export const loginLoginAccessToken = <ThrowOnError extends boolean = false>(
	options: Options<LoginLoginAccessTokenData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		LoginLoginAccessTokenResponse,
		LoginLoginAccessTokenError,
		ThrowOnError
	>({
		...options,
		...urlSearchParamsBodySerializer,
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
			...options?.headers
		},
		url: '/api/v1/login/access-token'
	});
};

/**
 * Test Token
 * Test access token
 */
export const loginTestToken = <ThrowOnError extends boolean = false>(
	options?: Options<unknown, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		LoginTestTokenResponse,
		LoginTestTokenError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/login/test-token'
	});
};

/**
 * Recover Password
 * Password Recovery
 */
export const loginRecoverPassword = <ThrowOnError extends boolean = false>(
	options: Options<LoginRecoverPasswordData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		LoginRecoverPasswordResponse,
		LoginRecoverPasswordError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/password-recovery/{email}'
	});
};

/**
 * Reset Password
 * Reset password
 */
export const loginResetPassword = <ThrowOnError extends boolean = false>(
	options: Options<LoginResetPasswordData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		LoginResetPasswordResponse,
		LoginResetPasswordError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/reset-password/'
	});
};

/**
 * Recover Password Html Content
 * HTML Content for Password Recovery
 */
export const loginRecoverPasswordHtmlContent = <ThrowOnError extends boolean = false>(
	options: Options<LoginRecoverPasswordHtmlContentData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		LoginRecoverPasswordHtmlContentResponse,
		LoginRecoverPasswordHtmlContentError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/password-recovery-html-content/{email}'
	});
};

/**
 * Read Users
 * Retrieve users.
 */
export const usersReadUsers = <ThrowOnError extends boolean = false>(
	options?: Options<UsersReadUsersData, ThrowOnError>
) => {
	return (options?.client ?? client).get<UsersReadUsersResponse, UsersReadUsersError, ThrowOnError>(
		{
			...options,
			url: '/api/v1/users/'
		}
	);
};

/**
 * Create User
 * Create new user.
 */
export const usersCreateUser = <ThrowOnError extends boolean = false>(
	options: Options<UsersCreateUserData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		UsersCreateUserResponse,
		UsersCreateUserError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/'
	});
};

/**
 * Read User Me
 * Get current user.
 */
export const usersReadUserMe = <ThrowOnError extends boolean = false>(
	options?: Options<unknown, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		UsersReadUserMeResponse,
		UsersReadUserMeError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/me'
	});
};

/**
 * Delete User Me
 * Delete own user.
 */
export const usersDeleteUserMe = <ThrowOnError extends boolean = false>(
	options?: Options<unknown, ThrowOnError>
) => {
	return (options?.client ?? client).delete<
		UsersDeleteUserMeResponse,
		UsersDeleteUserMeError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/me'
	});
};

/**
 * Update User Me
 * Update own user.
 */
export const usersUpdateUserMe = <ThrowOnError extends boolean = false>(
	options: Options<UsersUpdateUserMeData, ThrowOnError>
) => {
	return (options?.client ?? client).patch<
		UsersUpdateUserMeResponse,
		UsersUpdateUserMeError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/me'
	});
};

/**
 * Update Password Me
 * Update own password.
 */
export const usersUpdatePasswordMe = <ThrowOnError extends boolean = false>(
	options: Options<UsersUpdatePasswordMeData, ThrowOnError>
) => {
	return (options?.client ?? client).patch<
		UsersUpdatePasswordMeResponse,
		UsersUpdatePasswordMeError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/me/password'
	});
};

/**
 * Register User
 * Create new user without the need to be logged in.
 */
export const usersRegisterUser = <ThrowOnError extends boolean = false>(
	options: Options<UsersRegisterUserData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		UsersRegisterUserResponse,
		UsersRegisterUserError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/signup'
	});
};

/**
 * Read User By Id
 * Get a specific user by id.
 */
export const usersReadUserById = <ThrowOnError extends boolean = false>(
	options: Options<UsersReadUserByIdData, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		UsersReadUserByIdResponse,
		UsersReadUserByIdError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/{user_id}'
	});
};

/**
 * Update User
 * Update a user.
 */
export const usersUpdateUser = <ThrowOnError extends boolean = false>(
	options: Options<UsersUpdateUserData, ThrowOnError>
) => {
	return (options?.client ?? client).patch<
		UsersUpdateUserResponse,
		UsersUpdateUserError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/{user_id}'
	});
};

/**
 * Delete User
 * Delete a user.
 */
export const usersDeleteUser = <ThrowOnError extends boolean = false>(
	options: Options<UsersDeleteUserData, ThrowOnError>
) => {
	return (options?.client ?? client).delete<
		UsersDeleteUserResponse,
		UsersDeleteUserError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/users/{user_id}'
	});
};

/**
 * Test Email
 * Test emails.
 */
export const utilsTestEmail = <ThrowOnError extends boolean = false>(
	options: Options<UtilsTestEmailData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		UtilsTestEmailResponse,
		UtilsTestEmailError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/utils/test-email/'
	});
};

/**
 * Health Check
 */
export const utilsHealthCheck = <ThrowOnError extends boolean = false>(
	options?: Options<unknown, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		UtilsHealthCheckResponse,
		UtilsHealthCheckError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/utils/health-check/'
	});
};

/**
 * Read Items
 * Retrieve items.
 */
export const itemsReadItems = <ThrowOnError extends boolean = false>(
	options?: Options<ItemsReadItemsData, ThrowOnError>
) => {
	return (options?.client ?? client).get<ItemsReadItemsResponse, ItemsReadItemsError, ThrowOnError>(
		{
			...options,
			url: '/api/v1/items/'
		}
	);
};

/**
 * Create Item
 * Create new item.
 */
export const itemsCreateItem = <ThrowOnError extends boolean = false>(
	options: Options<ItemsCreateItemData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		ItemsCreateItemResponse,
		ItemsCreateItemError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/items/'
	});
};

/**
 * Read Item
 * Get item by ID.
 */
export const itemsReadItem = <ThrowOnError extends boolean = false>(
	options: Options<ItemsReadItemData, ThrowOnError>
) => {
	return (options?.client ?? client).get<ItemsReadItemResponse, ItemsReadItemError, ThrowOnError>({
		...options,
		url: '/api/v1/items/{id}'
	});
};

/**
 * Update Item
 * Update an item.
 */
export const itemsUpdateItem = <ThrowOnError extends boolean = false>(
	options: Options<ItemsUpdateItemData, ThrowOnError>
) => {
	return (options?.client ?? client).put<
		ItemsUpdateItemResponse,
		ItemsUpdateItemError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/items/{id}'
	});
};

/**
 * Delete Item
 * Delete an item.
 */
export const itemsDeleteItem = <ThrowOnError extends boolean = false>(
	options: Options<ItemsDeleteItemData, ThrowOnError>
) => {
	return (options?.client ?? client).delete<
		ItemsDeleteItemResponse,
		ItemsDeleteItemError,
		ThrowOnError
	>({
		...options,
		url: '/api/v1/items/{id}'
	});
};