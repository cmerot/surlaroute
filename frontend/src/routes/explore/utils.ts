import type {
	EventPointFeature,
	OrgPublic,
	PersonPublic,
	TourFeatureCollection,
	TourLineFeature,
	TourPublic,
} from "$lib/backend/client";
import type { BBox, FeatureCollection } from "geojson";
import type { LngLatBounds, LngLatBoundsLike } from "maplibre-gl";

function roundTo(value: number, precision: number) {
	return Math.round(value * 10 ** precision) / 10 ** precision;
}

export function boundsTo2D(bounds: BBox): [number, number, number, number] {
	if (bounds.length === 4) {
		return bounds;
	} else {
		console.error("bounds is not a BBox2D", bounds);
	}
	// skip z at index 2 and 5
	return [bounds[0], bounds[1], bounds[3], bounds[4]];
}

export function lonLngTo2D(lonLng: [number, number, number] | [number, number]): [number, number] {
	if (lonLng.length === 2) {
		return lonLng;
	} else {
		console.error("lonLng is not a Point2D", lonLng);
	}
	// skip z at index 2
	return [lonLng[0], lonLng[1]];
}

export interface Center {
	lng: number;
	lat: number;
	zoom: number;
}

export interface GeoQueryBase {
	center?: Center;
	bounds?: BBox;
}

export type GeoQuery = GeoQueryBase & { bounds: BBox };

export type EntityResult =
	| {
			type: "Org";
			value: OrgPublic;
	  }
	| {
			type: "Person";
			value: PersonPublic;
	  }
	| {
			type: "Tour";
			value: TourPublic;
	  };

export type Results = {
	slr: TourFeatureCollection[];
	nominatim?: FeatureCollection;
	entity?: EntityResult;
};

/**
 * Typeguard for LngLatBounds, as there's like a bug:
 * <MapLibre {bounds} /> is typed as LngLatBoundsLike, which include
 * LngLatBounds, but the editor does not understand that.
 *
 * @param obj - The object to check
 * @returns True if the object is a LngLatBounds, false otherwise
 */
export function isLngLatBounds(obj: LngLatBoundsLike | undefined): obj is LngLatBounds {
	if (!obj) return false;
	return typeof (obj as LngLatBounds).getSouthWest === "function";
}

export function encodeCenterString(coordinates: Center): string {
	return `${coordinates.lat},${coordinates.lng},${coordinates.zoom}z`;
}

export function decodeCenterString(coordinates: string): Center {
	const [lat, lng, zoom] = coordinates.split(",");
	return {
		lat: roundTo(parseFloat(lat), 3),
		lng: roundTo(parseFloat(lng), 3),
		zoom: roundTo(parseFloat(zoom), 2),
	};
}

export interface MapPosition {
	lat: number;
	lon: number;
	zoom: number;
}

export function parseUrlSearch(search: string): MapPosition | null {
	const match = search.match(/^\?@(-?\d+\.?\d*),(-?\d+\.?\d*),(\d+\.?\d*)/);

	if (!match) return null;

	const [, lat, lon, zoom] = match;

	return {
		lat: parseFloat(lat),
		lon: parseFloat(lon),
		zoom: parseFloat(zoom),
	};
}
export function decodeBoundsString(bounds: string): LngLatBoundsLike {
	const [w, s, e, n] = bounds.split(",");
	return [parseFloat(w), parseFloat(s), parseFloat(e), parseFloat(n)];
}

export function encodeBoundsString(bounds: BBox): string {
	return bounds.join(",");
}

export function mergeBoundingBoxes(boxes: Array<BBox>): BBox {
	if (boxes.length === 0) {
		return [0, 0, 0, 0];
	}
	return boxes.reduce((merged, current) => {
		const [minLat, maxLat, minLon, maxLon] = merged;
		const [curMinLat, curMaxLat, curMinLon, curMaxLon] = current;

		return [
			Math.min(minLat, curMinLat),
			Math.max(maxLat, curMaxLat),
			Math.min(minLon, curMinLon),
			Math.max(maxLon, curMaxLon),
		];
	}) as BBox;
}

const zooms = {
	amenity: 16,
	tourism: 16,
	railway: 16,
	place: 16,
	hamlet: 15,
	neighbourhood: 15,
	suburb: 13,
	city: 12,
	city_district: 10,
	postcode: 9,
	county: 8,
	state: 6,
	country: 5,
};

export function getZoomByAddressType(addressType: string) {
	return zooms[addressType as keyof typeof zooms] || 10;
}

export function isEventFeature(
	feature: TourLineFeature | EventPointFeature,
): feature is EventPointFeature {
	return feature.properties.type === "event_point";
}
