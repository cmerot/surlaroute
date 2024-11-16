import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],
	// server: {
	// 	proxy: {
	// 		'/api': {
	// 			target: 'http://localhost:8000',
	// 			changeOrigin: true,
	// 			rewrite: (path) => {
	// 				return path.replace(/^\/api/, '/api/v1');
	// 			},
	// 			configure(proxy, options) {
	// 				proxy.on('proxyReq', (clientRequest) => {
	// 					sessionStore.dump();
	// 					console.log(clientRequest.getHeader('cookie'));
	// 				});
	// 				// console.log({ proxy, options });
	// 			}
	// 		}
	// 	}
	// },
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
