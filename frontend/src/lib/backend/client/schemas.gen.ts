// This file is auto-generated by @hey-api/openapi-ts

export const ActorAssocCreateSchema = {
	properties: {
		actor: {
			anyOf: [
				{
					$ref: '#/components/schemas/PersonCreate'
				},
				{
					$ref: '#/components/schemas/OrgCreate'
				},
				{
					type: 'null'
				}
			],
			title: 'Actor'
		}
	},
	type: 'object',
	title: 'ActorAssocCreate'
} as const;

export const ActorAssocPublicSchema = {
	properties: {
		actor: {
			anyOf: [
				{
					$ref: '#/components/schemas/PersonPublic'
				},
				{
					$ref: '#/components/schemas/OrgPublic'
				}
			],
			title: 'Actor'
		}
	},
	type: 'object',
	required: ['actor'],
	title: 'ActorAssocPublic',
	description: `used to map any many-to-many relation impliying an actor
ex: OrgActorAssoc requires an org and an actor, so to render
the relation we'll use this. If we use a more specialized
model with actor and org, there will be recursion:
Org.member_assocs.org.member_assocs.org, ...`
} as const;

export const ActorAssocUpdateSchema = {
	properties: {
		actor: {
			anyOf: [
				{
					$ref: '#/components/schemas/PersonUpdate'
				},
				{
					$ref: '#/components/schemas/OrgUpdate'
				},
				{
					type: 'null'
				}
			],
			title: 'Actor'
		}
	},
	type: 'object',
	title: 'ActorAssocUpdate'
} as const;

export const AddressGeoCreateSchema = {
	properties: {
		q: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Q'
		},
		street: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Street'
		},
		postal_code: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Postal Code'
		},
		city: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'City'
		},
		country: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Country'
		},
		geom_point: {
			anyOf: [
				{
					type: 'string'
				},
				{
					$ref: '#/components/schemas/Point'
				},
				{
					type: 'null'
				}
			],
			title: 'Geom Point'
		}
	},
	type: 'object',
	title: 'AddressGeoCreate'
} as const;

export const AddressGeoPublicSchema = {
	properties: {
		q: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Q'
		},
		street: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Street'
		},
		postal_code: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Postal Code'
		},
		city: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'City'
		},
		country: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Country'
		},
		geom_point: {
			anyOf: [
				{
					$ref: '#/components/schemas/Point'
				},
				{
					type: 'null'
				}
			],
			title: 'Geom Point'
		},
		id: {
			type: 'string',
			format: 'uuid',
			title: 'Id'
		}
	},
	type: 'object',
	required: ['id'],
	title: 'AddressGeoPublic'
} as const;

export const AddressGeoUpdateSchema = {
	properties: {
		q: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Q'
		},
		street: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Street'
		},
		postal_code: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Postal Code'
		},
		city: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'City'
		},
		country: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Country'
		},
		geom_point: {
			anyOf: [
				{
					type: 'string'
				},
				{
					$ref: '#/components/schemas/Point'
				},
				{
					type: 'null'
				}
			],
			title: 'Geom Point'
		}
	},
	type: 'object',
	title: 'AddressGeoUpdate'
} as const;

export const Body_login_access_tokenSchema = {
	properties: {
		grant_type: {
			anyOf: [
				{
					type: 'string',
					pattern: 'password'
				},
				{
					type: 'null'
				}
			],
			title: 'Grant Type'
		},
		username: {
			type: 'string',
			title: 'Username'
		},
		password: {
			type: 'string',
			title: 'Password'
		},
		scope: {
			type: 'string',
			title: 'Scope',
			default: ''
		},
		client_id: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Client Id'
		},
		client_secret: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Client Secret'
		}
	},
	type: 'object',
	required: ['username', 'password'],
	title: 'Body_login-access_token'
} as const;

export const ContactCreateSchema = {
	properties: {
		email_address: {
			anyOf: [
				{
					type: 'string',
					format: 'email'
				},
				{
					type: 'null'
				}
			],
			title: 'Email Address'
		},
		phone_number: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Phone Number'
		},
		website: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'string',
					maxLength: 2083,
					minLength: 1,
					format: 'uri'
				},
				{
					type: 'null'
				}
			],
			title: 'Website'
		},
		address: {
			anyOf: [
				{
					$ref: '#/components/schemas/AddressGeoCreate'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	title: 'ContactCreate'
} as const;

export const ContactPublicSchema = {
	properties: {
		email_address: {
			anyOf: [
				{
					type: 'string',
					format: 'email'
				},
				{
					type: 'null'
				}
			],
			title: 'Email Address'
		},
		phone_number: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Phone Number'
		},
		website: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Website'
		},
		id: {
			type: 'string',
			format: 'uuid',
			title: 'Id'
		},
		address: {
			anyOf: [
				{
					$ref: '#/components/schemas/AddressGeoPublic'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	required: ['id'],
	title: 'ContactPublic'
} as const;

export const ContactUpdateSchema = {
	properties: {
		email_address: {
			anyOf: [
				{
					type: 'string',
					format: 'email'
				},
				{
					type: 'null'
				}
			],
			title: 'Email Address'
		},
		phone_number: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Phone Number'
		},
		website: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'string',
					maxLength: 2083,
					minLength: 1,
					format: 'uri'
				},
				{
					type: 'null'
				}
			],
			title: 'Website'
		},
		address: {
			anyOf: [
				{
					$ref: '#/components/schemas/AddressGeoUpdate'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	title: 'ContactUpdate'
} as const;

export const DeleteResponseSchema = {
	properties: {
		success: {
			type: 'boolean',
			title: 'Success'
		},
		data: {
			anyOf: [
				{},
				{
					type: 'null'
				}
			],
			title: 'Data'
		},
		message: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Message'
		}
	},
	type: 'object',
	required: ['success'],
	title: 'DeleteResponse',
	description: 'Response schema for any delete request.'
} as const;

export const EventPublicSchema = {
	properties: {
		description: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Description'
		},
		start_dt: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'string',
					format: 'date-time'
				},
				{
					type: 'null'
				}
			],
			title: 'Start Dt'
		},
		end_dt: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'string',
					format: 'date-time'
				},
				{
					type: 'null'
				}
			],
			title: 'End Dt'
		},
		id: {
			type: 'string',
			format: 'uuid',
			title: 'Id'
		},
		event_venue: {
			$ref: '#/components/schemas/OrgPublic'
		},
		actor_assocs: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/ActorAssocPublic'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Actor Assocs'
		}
	},
	type: 'object',
	required: ['id', 'event_venue'],
	title: 'EventPublic'
} as const;

export const HTTPValidationErrorSchema = {
	properties: {
		detail: {
			items: {
				$ref: '#/components/schemas/ValidationError'
			},
			type: 'array',
			title: 'Detail'
		}
	},
	type: 'object',
	title: 'HTTPValidationError'
} as const;

export const MessageSchema = {
	properties: {
		message: {
			type: 'string',
			title: 'Message'
		}
	},
	type: 'object',
	required: ['message'],
	title: 'Message'
} as const;

export const NewPasswordSchema = {
	properties: {
		token: {
			type: 'string',
			title: 'Token'
		},
		new_password: {
			type: 'string',
			maxLength: 40,
			minLength: 8,
			title: 'New Password'
		}
	},
	type: 'object',
	required: ['token', 'new_password'],
	title: 'NewPassword'
} as const;

export const OrgAssocPublicSchema = {
	properties: {
		org: {
			$ref: '#/components/schemas/OrgPublic'
		}
	},
	type: 'object',
	required: ['org'],
	title: 'OrgAssocPublic',
	description: 'same than ActorAssocPublic but for from the POV of an actor'
} as const;

export const OrgCreateSchema = {
	properties: {
		description: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Description'
		},
		name: {
			type: 'string',
			title: 'Name'
		},
		activities: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/TreeCreate'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Activities'
		},
		member_assocs: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/ActorAssocCreate'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Member Assocs'
		},
		contact: {
			anyOf: [
				{
					$ref: '#/components/schemas/ContactCreate'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	required: ['name'],
	title: 'OrgCreate'
} as const;

export const OrgPublicSchema = {
	properties: {
		description: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Description'
		},
		id: {
			type: 'string',
			format: 'uuid',
			title: 'Id'
		},
		name: {
			type: 'string',
			title: 'Name'
		},
		activities: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/TreePublic'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Activities'
		},
		member_assocs: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/ActorAssocPublic'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Member Assocs'
		},
		contact: {
			anyOf: [
				{
					$ref: '#/components/schemas/ContactPublic'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	required: ['id', 'name'],
	title: 'OrgPublic'
} as const;

export const OrgUpdateSchema = {
	properties: {
		description: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Description'
		},
		name: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Name'
		},
		activities: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/TreeUpdate'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Activities'
		},
		member_assocs: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/ActorAssocUpdate'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Member Assocs'
		},
		contact: {
			anyOf: [
				{
					$ref: '#/components/schemas/ContactUpdate'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	title: 'OrgUpdate'
} as const;

export const PagedResponse_OrgPublic_Schema = {
	properties: {
		total: {
			type: 'integer',
			title: 'Total'
		},
		limit: {
			type: 'integer',
			title: 'Limit'
		},
		offset: {
			type: 'integer',
			title: 'Offset'
		},
		results: {
			items: {
				$ref: '#/components/schemas/OrgPublic'
			},
			type: 'array',
			title: 'Results'
		}
	},
	type: 'object',
	required: ['total', 'limit', 'offset', 'results'],
	title: 'PagedResponse[OrgPublic]'
} as const;

export const PagedResponse_PersonPublic_Schema = {
	properties: {
		total: {
			type: 'integer',
			title: 'Total'
		},
		limit: {
			type: 'integer',
			title: 'Limit'
		},
		offset: {
			type: 'integer',
			title: 'Offset'
		},
		results: {
			items: {
				$ref: '#/components/schemas/PersonPublic'
			},
			type: 'array',
			title: 'Results'
		}
	},
	type: 'object',
	required: ['total', 'limit', 'offset', 'results'],
	title: 'PagedResponse[PersonPublic]'
} as const;

export const PagedResponse_TourPublic_Schema = {
	properties: {
		total: {
			type: 'integer',
			title: 'Total'
		},
		limit: {
			type: 'integer',
			title: 'Limit'
		},
		offset: {
			type: 'integer',
			title: 'Offset'
		},
		results: {
			items: {
				$ref: '#/components/schemas/TourPublic'
			},
			type: 'array',
			title: 'Results'
		}
	},
	type: 'object',
	required: ['total', 'limit', 'offset', 'results'],
	title: 'PagedResponse[TourPublic]'
} as const;

export const PagedResponse_TreePublic_Schema = {
	properties: {
		total: {
			type: 'integer',
			title: 'Total'
		},
		limit: {
			type: 'integer',
			title: 'Limit'
		},
		offset: {
			type: 'integer',
			title: 'Offset'
		},
		results: {
			items: {
				$ref: '#/components/schemas/TreePublic'
			},
			type: 'array',
			title: 'Results'
		}
	},
	type: 'object',
	required: ['total', 'limit', 'offset', 'results'],
	title: 'PagedResponse[TreePublic]'
} as const;

export const PagedResponse_UserPublic_Schema = {
	properties: {
		total: {
			type: 'integer',
			title: 'Total'
		},
		limit: {
			type: 'integer',
			title: 'Limit'
		},
		offset: {
			type: 'integer',
			title: 'Offset'
		},
		results: {
			items: {
				$ref: '#/components/schemas/UserPublic'
			},
			type: 'array',
			title: 'Results'
		}
	},
	type: 'object',
	required: ['total', 'limit', 'offset', 'results'],
	title: 'PagedResponse[UserPublic]'
} as const;

export const PersonCreateSchema = {
	properties: {
		name: {
			type: 'string',
			title: 'Name'
		},
		role: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Role'
		},
		contact: {
			anyOf: [
				{
					$ref: '#/components/schemas/ContactCreate'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	required: ['name'],
	title: 'PersonCreate'
} as const;

export const PersonPublicSchema = {
	properties: {
		name: {
			type: 'string',
			title: 'Name'
		},
		role: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Role'
		},
		id: {
			type: 'string',
			format: 'uuid',
			title: 'Id'
		},
		contact: {
			anyOf: [
				{
					$ref: '#/components/schemas/ContactPublic'
				},
				{
					type: 'null'
				}
			]
		},
		membership_assocs: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/OrgAssocPublic'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Membership Assocs'
		}
	},
	type: 'object',
	required: ['name', 'id'],
	title: 'PersonPublic'
} as const;

export const PersonUpdateSchema = {
	properties: {
		name: {
			type: 'string',
			title: 'Name'
		},
		role: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Role'
		},
		contact: {
			anyOf: [
				{
					$ref: '#/components/schemas/ContactUpdate'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	required: ['name'],
	title: 'PersonUpdate'
} as const;

export const PointSchema = {
	properties: {
		bbox: {
			anyOf: [
				{
					prefixItems: [
						{
							type: 'number'
						},
						{
							type: 'number'
						},
						{
							type: 'number'
						},
						{
							type: 'number'
						}
					],
					type: 'array',
					maxItems: 4,
					minItems: 4
				},
				{
					prefixItems: [
						{
							type: 'number'
						},
						{
							type: 'number'
						},
						{
							type: 'number'
						},
						{
							type: 'number'
						},
						{
							type: 'number'
						},
						{
							type: 'number'
						}
					],
					type: 'array',
					maxItems: 6,
					minItems: 6
				},
				{
					type: 'null'
				}
			],
			title: 'Bbox'
		},
		type: {
			type: 'string',
			enum: ['Point'],
			const: 'Point',
			title: 'Type'
		},
		coordinates: {
			anyOf: [
				{
					$ref: '#/components/schemas/Position2D'
				},
				{
					$ref: '#/components/schemas/Position3D'
				}
			],
			title: 'Coordinates'
		}
	},
	type: 'object',
	required: ['type', 'coordinates'],
	title: 'Point',
	description: 'Point Model'
} as const;

export const Position2DSchema = {
	prefixItems: [
		{
			type: 'number',
			title: 'Longitude'
		},
		{
			type: 'number',
			title: 'Latitude'
		}
	],
	type: 'array',
	maxItems: 2,
	minItems: 2
} as const;

export const Position3DSchema = {
	prefixItems: [
		{
			type: 'number',
			title: 'Longitude'
		},
		{
			type: 'number',
			title: 'Latitude'
		},
		{
			type: 'number',
			title: 'Altitude'
		}
	],
	type: 'array',
	maxItems: 3,
	minItems: 3
} as const;

export const TokenSchema = {
	properties: {
		access_token: {
			type: 'string',
			title: 'Access Token'
		},
		token_type: {
			type: 'string',
			title: 'Token Type',
			default: 'bearer'
		}
	},
	type: 'object',
	required: ['access_token'],
	title: 'Token'
} as const;

export const TourPublicSchema = {
	properties: {
		name: {
			type: 'string',
			title: 'Name'
		},
		description: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Description'
		},
		year: {
			anyOf: [
				{
					type: 'integer'
				},
				{
					type: 'null'
				}
			],
			title: 'Year'
		},
		id: {
			type: 'string',
			format: 'uuid',
			title: 'Id'
		},
		events: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/EventPublic'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Events'
		},
		disciplines: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/TreePublic'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Disciplines'
		},
		mobilities: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/TreePublic'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Mobilities'
		},
		actor_assocs: {
			anyOf: [
				{
					items: {
						$ref: '#/components/schemas/ActorAssocPublic'
					},
					type: 'array'
				},
				{
					type: 'null'
				}
			],
			title: 'Actor Assocs'
		}
	},
	type: 'object',
	required: ['name', 'id'],
	title: 'TourPublic'
} as const;

export const TreeCreateSchema = {
	properties: {
		path: {
			type: 'string',
			title: 'Path',
			examples: ['some.path']
		},
		name: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Name'
		}
	},
	type: 'object',
	required: ['path'],
	title: 'TreeCreate'
} as const;

export const TreePublicSchema = {
	properties: {
		id: {
			anyOf: [
				{
					type: 'string',
					format: 'uuid'
				},
				{
					type: 'null'
				}
			],
			title: 'Id'
		},
		path: {
			type: 'string',
			minLength: 1,
			title: 'Path',
			examples: ['some.path']
		},
		name: {
			type: 'string',
			title: 'Name'
		}
	},
	type: 'object',
	required: ['path', 'name'],
	title: 'TreePublic'
} as const;

export const TreeUpdateSchema = {
	properties: {
		dest_path: {
			anyOf: [
				{
					type: 'string',
					minLength: 1,
					examples: ['some.path']
				},
				{
					type: 'null'
				}
			],
			title: 'Dest Path'
		},
		name: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Name'
		}
	},
	type: 'object',
	title: 'TreeUpdate'
} as const;

export const UpdateResponse_OrgPublic_Schema = {
	properties: {
		success: {
			type: 'boolean',
			title: 'Success'
		},
		data: {
			anyOf: [
				{
					$ref: '#/components/schemas/OrgPublic'
				},
				{
					type: 'null'
				}
			]
		},
		message: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Message'
		}
	},
	type: 'object',
	required: ['success'],
	title: 'UpdateResponse[OrgPublic]'
} as const;

export const UpdateResponse_PersonPublic_Schema = {
	properties: {
		success: {
			type: 'boolean',
			title: 'Success'
		},
		data: {
			anyOf: [
				{
					$ref: '#/components/schemas/PersonPublic'
				},
				{
					type: 'null'
				}
			]
		},
		message: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Message'
		}
	},
	type: 'object',
	required: ['success'],
	title: 'UpdateResponse[PersonPublic]'
} as const;

export const UpdateResponse_TreePublic_Schema = {
	properties: {
		success: {
			type: 'boolean',
			title: 'Success'
		},
		data: {
			anyOf: [
				{
					$ref: '#/components/schemas/TreePublic'
				},
				{
					type: 'null'
				}
			]
		},
		message: {
			anyOf: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			],
			title: 'Message'
		}
	},
	type: 'object',
	required: ['success'],
	title: 'UpdateResponse[TreePublic]'
} as const;

export const UserCreateSchema = {
	properties: {
		email: {
			type: 'string',
			maxLength: 255,
			format: 'email',
			title: 'Email'
		},
		is_active: {
			type: 'boolean',
			title: 'Is Active',
			default: false
		},
		is_superuser: {
			type: 'boolean',
			title: 'Is Superuser',
			default: false
		},
		is_member: {
			type: 'boolean',
			title: 'Is Member',
			default: false
		},
		password: {
			type: 'string',
			maxLength: 40,
			minLength: 8,
			title: 'Password'
		}
	},
	type: 'object',
	required: ['email', 'password'],
	title: 'UserCreate'
} as const;

export const UserPublicSchema = {
	properties: {
		email: {
			type: 'string',
			maxLength: 255,
			format: 'email',
			title: 'Email'
		},
		is_active: {
			type: 'boolean',
			title: 'Is Active'
		},
		is_superuser: {
			type: 'boolean',
			title: 'Is Superuser'
		},
		is_member: {
			type: 'boolean',
			title: 'Is Member'
		},
		id: {
			type: 'string',
			format: 'uuid',
			title: 'Id'
		},
		person: {
			anyOf: [
				{
					$ref: '#/components/schemas/PersonPublic'
				},
				{
					type: 'null'
				}
			]
		}
	},
	type: 'object',
	required: ['email', 'is_active', 'is_superuser', 'is_member', 'id'],
	title: 'UserPublic'
} as const;

export const UserRegisterSchema = {
	properties: {
		email: {
			type: 'string',
			maxLength: 255,
			format: 'email',
			title: 'Email'
		},
		password: {
			type: 'string',
			maxLength: 40,
			minLength: 8,
			title: 'Password'
		}
	},
	type: 'object',
	required: ['email', 'password'],
	title: 'UserRegister'
} as const;

export const UserUpdateSchema = {
	properties: {
		email: {
			anyOf: [
				{
					type: 'string',
					maxLength: 255,
					format: 'email'
				},
				{
					type: 'null'
				}
			],
			title: 'Email'
		},
		is_active: {
			type: 'boolean',
			title: 'Is Active',
			default: false
		},
		is_superuser: {
			type: 'boolean',
			title: 'Is Superuser',
			default: false
		},
		is_member: {
			type: 'boolean',
			title: 'Is Member',
			default: false
		},
		password: {
			anyOf: [
				{
					type: 'string',
					maxLength: 40,
					minLength: 8
				},
				{
					type: 'null'
				}
			],
			title: 'Password'
		}
	},
	type: 'object',
	title: 'UserUpdate'
} as const;

export const ValidationErrorSchema = {
	properties: {
		loc: {
			items: {
				anyOf: [
					{
						type: 'string'
					},
					{
						type: 'integer'
					}
				]
			},
			type: 'array',
			title: 'Location'
		},
		msg: {
			type: 'string',
			title: 'Message'
		},
		type: {
			type: 'string',
			title: 'Error Type'
		}
	},
	type: 'object',
	required: ['loc', 'msg', 'type'],
	title: 'ValidationError'
} as const;
