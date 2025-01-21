import {
	directoryGetOrg,
	directoryGetPerson,
	exploreGetData,
	toursGetTour,
} from "$lib/backend/client/sdk.gen";
import { getErrorMessage } from "$lib/slr-utils";
import type { FeatureCollection } from "geojson";
import type { PageServerLoad } from "./$types";
import {
	decodeBoundsString,
	decodeCenterString,
	type EntityResult,
	type GeoQuery,
	type GeoQueryBase,
	type Results,
} from "./utils";

/**
 * Nominatim (OSM) geocoder, ready to use for our Map
 * @private
 */
async function forwardGeocodingNominatim(
	client: typeof fetch,
	q: string,
	viewbox: string = "",
): Promise<FeatureCollection> {
	// Transform parameters into Nominatim format
	const params: Record<string, string> = {
		q: q,
		countrycodes: "be,ch,de,es,fr,it,nl",
		limit: "10",
		format: "geojson",
		polygon_geojson: "1",
		addressdetails: "1",
		viewbox,
	};
	const baseUrl = "https://nominatim.openstreetmap.org/search?";
	const searchParams = new URLSearchParams(params);
	console.log("searchParams", `${baseUrl}${searchParams.toString()}`);
	const res = await client(`${baseUrl}${searchParams.toString()}`);
	const data = await res.json();
	return data;
}

async function getEntity(
	id: string,
	type: string,
	authToken: string | undefined,
): Promise<EntityResult | null> {
	switch (type) {
		case "Org": {
			const result = await directoryGetOrg({
				path: { id },
				headers: {
					Authorization: `Bearer ${authToken}`,
				},
			});
			if (result.error) {
				console.error(result.response.status, getErrorMessage(result.error));
				return null;
			}
			return { type, value: result.data };
		}
		case "Person": {
			const result = await directoryGetPerson({
				path: { id },
				headers: {
					Authorization: `Bearer ${authToken}`,
				},
			});
			if (result.error) {
				console.error(result.response.status, getErrorMessage(result.error));
				return null;
			}
			return { type, value: result.data };
		}
		case "Tour": {
			const result = await toursGetTour({
				path: { id },
				headers: {
					Authorization: `Bearer ${authToken}`,
				},
			});
			if (result.error) {
				console.error(result.response.status, getErrorMessage(result.error));
				return null;
			}
			return { type, value: result.data };
		}
		default:
			return null;
	}
}

function buildGeoQuery(params: { center?: string; bounds?: string }): GeoQuery {
	// default bounds: bounds:-5.1978240,42.1583536,9.0493105,51.6488428
	const baseQuery: GeoQueryBase = {
		// center: {
		// 	lat: 46.3398967,
		// 	lng: 3.3996692,
		// 	zoom: 5.21,
		// },
		// bounds: [-5.4117538, 41.7436202, 10.253668, 52.1611514],
		bounds: [-5.1168957, 41.2652227, 9.8566018, 51.4183293],
	};

	if (params.center) {
		baseQuery.center = decodeCenterString(params.center);
	}

	if (params.bounds) {
		baseQuery.bounds = decodeBoundsString(params.bounds);
	}

	return baseQuery as GeoQuery;
}
export const load: PageServerLoad = async ({ url, locals, fetch }) => {
	// Center coordinates
	const center = url.searchParams.get("c") || undefined;

	// Bbox -> used to filter results
	const bounds = url.searchParams.get("b") || undefined;

	const geoQuery: GeoQuery = buildGeoQuery({ center: center, bounds: bounds });

	const mobilityPath = url.searchParams.get("m") || undefined;

	// Search results
	const results: Partial<Results> = {};

	// Nominatim search
	const textQuery = url.searchParams.get("q") || undefined;
	if (textQuery) {
		console.log("Nominatim search");
		const nominatimResult = await forwardGeocodingNominatim(fetch, textQuery, bounds);
		results.nominatim = nominatimResult;
	}

	// SLR search
	console.log("SLR exploreGetData");
	const slrResult = await exploreGetData({
		headers: {
			Authorization: `Bearer ${locals.authToken}`,
		},
		query: { bbox: geoQuery.bounds.join(","), mobility_path: mobilityPath },
	});

	if (slrResult.error) {
		console.error(slrResult.response.status, getErrorMessage(slrResult.error));
	} else {
		results.slr = slrResult.data;
	}

	// Entity
	const entityId = url.searchParams.get("e") || undefined;
	const entityType = url.searchParams.get("t") || undefined;
	if (entityId && entityType) {
		console.log("SLR getEntity");
		const entity = await getEntity(entityId, entityType, locals.authToken);
		if (entity) {
			results.entity = entity;
		}
	}

	const response: {
		query: {
			geo: GeoQuery;
			q?: string;
			m?: string;
		};
		results: Results;
	} = {
		query: {
			geo: geoQuery,
			q: textQuery,
			m: mobilityPath,
		},
		results: results as Results,
	};

	return response;
};
