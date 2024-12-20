// This file is auto-generated by @hey-api/openapi-ts

import {
	createClient,
	createConfig,
	type Options,
	urlSearchParamsBodySerializer
} from '@hey-api/client-fetch';
import type {
	LoginAccessTokenData,
	LoginAccessTokenError,
	LoginAccessTokenResponse,
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
	UsersReadData,
	UsersReadError,
	UsersReadResponse,
	UsersCreateData,
	UsersCreateError,
	UsersCreateResponse,
	UsersReadUserMeError,
	UsersReadUserMeResponse,
	UsersRegisterData,
	UsersRegisterError,
	UsersRegisterResponse,
	UsersReadByIdData,
	UsersReadByIdError,
	UsersReadByIdResponse,
	UsersUpdateData,
	UsersUpdateError,
	UsersUpdateResponse,
	UsersDeleteData,
	UsersDeleteError,
	UsersDeleteResponse,
	UtilsTestEmailData,
	UtilsTestEmailError,
	UtilsTestEmailResponse,
	UtilsHealthCheckError,
	UtilsHealthCheckResponse,
	ActivitiesCreateActivityData,
	ActivitiesCreateActivityError,
	ActivitiesCreateActivityResponse,
	ActivitiesReadActivitiesData,
	ActivitiesReadActivitiesError,
	ActivitiesReadActivitiesResponse,
	ActivitiesReadActivitiesByPathData,
	ActivitiesReadActivitiesByPathError,
	ActivitiesReadActivitiesByPathResponse,
	ActivitiesUpdateActivityData,
	ActivitiesUpdateActivityError,
	ActivitiesUpdateActivityResponse,
	ActivitiesDeleteActivityData,
	ActivitiesDeleteActivityError,
	ActivitiesDeleteActivityResponse,
	PeopleCreatePersonData,
	PeopleCreatePersonError,
	PeopleCreatePersonResponse,
	PeopleReadPeopleData,
	PeopleReadPeopleError,
	PeopleReadPeopleResponse,
	PeopleReadPersonByIdData,
	PeopleReadPersonByIdError,
	PeopleReadPersonByIdResponse,
	PeopleUpdatePersonData,
	PeopleUpdatePersonError,
	PeopleUpdatePersonResponse,
	PeopleDeletePersonData,
	PeopleDeletePersonError,
	PeopleDeletePersonResponse,
	OrgsCreateOrgData,
	OrgsCreateOrgError,
	OrgsCreateOrgResponse,
	OrgsReadOrgsData,
	OrgsReadOrgsError,
	OrgsReadOrgsResponse,
	OrgsReadOrgByIdData,
	OrgsReadOrgByIdError,
	OrgsReadOrgByIdResponse,
	OrgsUpdateOrgData,
	OrgsUpdateOrgError,
	OrgsUpdateOrgResponse,
	OrgsDeleteOrgData,
	OrgsDeleteOrgError,
	OrgsDeleteOrgResponse,
	ToursReadTourByIdData,
	ToursReadTourByIdError,
	ToursReadTourByIdResponse,
	ToursReadToursData,
	ToursReadToursError,
	ToursReadToursResponse
} from './types.gen';

export const client = createClient(createConfig());

/**
 * Access Token
 * OAuth2 compatible token login, get an access token for future requests
 */
export const loginAccessToken = <ThrowOnError extends boolean = false>(
	options: Options<LoginAccessTokenData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		LoginAccessTokenResponse,
		LoginAccessTokenError,
		ThrowOnError
	>({
		...options,
		...urlSearchParamsBodySerializer,
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
			...options?.headers
		},
		url: '/api/login/access-token'
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
		url: '/api/login/test-token'
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
		url: '/api/password-recovery/{email}'
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
		url: '/api/reset-password/'
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
		url: '/api/password-recovery-html-content/{email}'
	});
};

/**
 * Read
 * Read users.
 */
export const usersRead = <ThrowOnError extends boolean = false>(
	options?: Options<UsersReadData, ThrowOnError>
) => {
	return (options?.client ?? client).get<UsersReadResponse, UsersReadError, ThrowOnError>({
		...options,
		url: '/api/users/'
	});
};

/**
 * Create
 * Create new user.
 */
export const usersCreate = <ThrowOnError extends boolean = false>(
	options: Options<UsersCreateData, ThrowOnError>
) => {
	return (options?.client ?? client).post<UsersCreateResponse, UsersCreateError, ThrowOnError>({
		...options,
		url: '/api/users/'
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
		url: '/api/users/me'
	});
};

/**
 * Register
 * Create new user without the need to be logged in.
 */
export const usersRegister = <ThrowOnError extends boolean = false>(
	options: Options<UsersRegisterData, ThrowOnError>
) => {
	return (options?.client ?? client).post<UsersRegisterResponse, UsersRegisterError, ThrowOnError>({
		...options,
		url: '/api/users/signup'
	});
};

/**
 * Read By Id
 * Get a specific user by id.
 */
export const usersReadById = <ThrowOnError extends boolean = false>(
	options: Options<UsersReadByIdData, ThrowOnError>
) => {
	return (options?.client ?? client).get<UsersReadByIdResponse, UsersReadByIdError, ThrowOnError>({
		...options,
		url: '/api/users/{user_id}'
	});
};

/**
 * Update
 * Update a user.
 */
export const usersUpdate = <ThrowOnError extends boolean = false>(
	options: Options<UsersUpdateData, ThrowOnError>
) => {
	return (options?.client ?? client).patch<UsersUpdateResponse, UsersUpdateError, ThrowOnError>({
		...options,
		url: '/api/users/{user_id}'
	});
};

/**
 * Delete
 * Delete a user.
 */
export const usersDelete = <ThrowOnError extends boolean = false>(
	options: Options<UsersDeleteData, ThrowOnError>
) => {
	return (options?.client ?? client).delete<UsersDeleteResponse, UsersDeleteError, ThrowOnError>({
		...options,
		url: '/api/users/{user_id}'
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
		url: '/api/utils/test-email/'
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
		url: '/api/utils/health-check/'
	});
};

/**
 * Create Activity
 * Create an activity.
 */
export const activitiesCreateActivity = <ThrowOnError extends boolean = false>(
	options: Options<ActivitiesCreateActivityData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		ActivitiesCreateActivityResponse,
		ActivitiesCreateActivityError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/activities/'
	});
};

/**
 * Read Activities
 * Read all activities.
 */
export const activitiesReadActivities = <ThrowOnError extends boolean = false>(
	options?: Options<ActivitiesReadActivitiesData, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		ActivitiesReadActivitiesResponse,
		ActivitiesReadActivitiesError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/activities/'
	});
};

/**
 * Read Activities By Path
 * Read activities from a path.
 */
export const activitiesReadActivitiesByPath = <ThrowOnError extends boolean = false>(
	options: Options<ActivitiesReadActivitiesByPathData, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		ActivitiesReadActivitiesByPathResponse,
		ActivitiesReadActivitiesByPathError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/activities/{path}'
	});
};

/**
 * Update Activity
 * Update an activity.
 *
 * If the name or the parent path is patched, it will also update children.
 */
export const activitiesUpdateActivity = <ThrowOnError extends boolean = false>(
	options: Options<ActivitiesUpdateActivityData, ThrowOnError>
) => {
	return (options?.client ?? client).patch<
		ActivitiesUpdateActivityResponse,
		ActivitiesUpdateActivityError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/activities/{path}'
	});
};

/**
 * Delete Activity
 * Delete an activity and its children.
 */
export const activitiesDeleteActivity = <ThrowOnError extends boolean = false>(
	options: Options<ActivitiesDeleteActivityData, ThrowOnError>
) => {
	return (options?.client ?? client).delete<
		ActivitiesDeleteActivityResponse,
		ActivitiesDeleteActivityError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/activities/{path}'
	});
};

/**
 * Create Person
 * Create a person.
 */
export const peopleCreatePerson = <ThrowOnError extends boolean = false>(
	options: Options<PeopleCreatePersonData, ThrowOnError>
) => {
	return (options?.client ?? client).post<
		PeopleCreatePersonResponse,
		PeopleCreatePersonError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/people/'
	});
};

/**
 * Read People
 * Read paginated people.
 */
export const peopleReadPeople = <ThrowOnError extends boolean = false>(
	options?: Options<PeopleReadPeopleData, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		PeopleReadPeopleResponse,
		PeopleReadPeopleError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/people/'
	});
};

/**
 * Read Person By Id
 * Read a person by its id.
 */
export const peopleReadPersonById = <ThrowOnError extends boolean = false>(
	options: Options<PeopleReadPersonByIdData, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		PeopleReadPersonByIdResponse,
		PeopleReadPersonByIdError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/people/{id}'
	});
};

/**
 * Update Person
 * Update a person.
 */
export const peopleUpdatePerson = <ThrowOnError extends boolean = false>(
	options: Options<PeopleUpdatePersonData, ThrowOnError>
) => {
	return (options?.client ?? client).patch<
		PeopleUpdatePersonResponse,
		PeopleUpdatePersonError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/people/{id}'
	});
};

/**
 * Delete Person
 * Delete a person.
 */
export const peopleDeletePerson = <ThrowOnError extends boolean = false>(
	options: Options<PeopleDeletePersonData, ThrowOnError>
) => {
	return (options?.client ?? client).delete<
		PeopleDeletePersonResponse,
		PeopleDeletePersonError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/people/{id}'
	});
};

/**
 * Create Org
 * Create an org.
 */
export const orgsCreateOrg = <ThrowOnError extends boolean = false>(
	options: Options<OrgsCreateOrgData, ThrowOnError>
) => {
	return (options?.client ?? client).post<OrgsCreateOrgResponse, OrgsCreateOrgError, ThrowOnError>({
		...options,
		url: '/api/directory/orgs/'
	});
};

/**
 * Read Orgs
 * Read paginated orgs.
 */
export const orgsReadOrgs = <ThrowOnError extends boolean = false>(
	options?: Options<OrgsReadOrgsData, ThrowOnError>
) => {
	return (options?.client ?? client).get<OrgsReadOrgsResponse, OrgsReadOrgsError, ThrowOnError>({
		...options,
		url: '/api/directory/orgs/'
	});
};

/**
 * Read Org By Id
 * Read an org by its id.
 */
export const orgsReadOrgById = <ThrowOnError extends boolean = false>(
	options: Options<OrgsReadOrgByIdData, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		OrgsReadOrgByIdResponse,
		OrgsReadOrgByIdError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/orgs/{id}'
	});
};

/**
 * Update Org
 * Update an org.
 */
export const orgsUpdateOrg = <ThrowOnError extends boolean = false>(
	options: Options<OrgsUpdateOrgData, ThrowOnError>
) => {
	return (options?.client ?? client).patch<OrgsUpdateOrgResponse, OrgsUpdateOrgError, ThrowOnError>(
		{
			...options,
			url: '/api/directory/orgs/{id}'
		}
	);
};

/**
 * Delete Org
 * Delete an org.
 */
export const orgsDeleteOrg = <ThrowOnError extends boolean = false>(
	options: Options<OrgsDeleteOrgData, ThrowOnError>
) => {
	return (options?.client ?? client).delete<
		OrgsDeleteOrgResponse,
		OrgsDeleteOrgError,
		ThrowOnError
	>({
		...options,
		url: '/api/directory/orgs/{id}'
	});
};

/**
 * Read Tour By Id
 * Read an tour by its id.
 */
export const toursReadTourById = <ThrowOnError extends boolean = false>(
	options: Options<ToursReadTourByIdData, ThrowOnError>
) => {
	return (options?.client ?? client).get<
		ToursReadTourByIdResponse,
		ToursReadTourByIdError,
		ThrowOnError
	>({
		...options,
		url: '/api/tours/{id}'
	});
};

/**
 * Read Tours
 * Read paginated tours.
 */
export const toursReadTours = <ThrowOnError extends boolean = false>(
	options?: Options<ToursReadToursData, ThrowOnError>
) => {
	return (options?.client ?? client).get<ToursReadToursResponse, ToursReadToursError, ThrowOnError>(
		{
			...options,
			url: '/api/tours/'
		}
	);
};
