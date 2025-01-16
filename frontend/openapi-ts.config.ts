import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
	client: '@hey-api/client-fetch',
	input: 'src/lib/backend/openapi.json',
	output: {
		path: 'src/lib/backend/client',
		format: 'biome',
		lint: 'biome'
	}
});
