import type { Config } from 'tailwindcss';
import { fontFamily } from 'tailwindcss/defaultTheme';

const config: Config = {
	darkMode: ['class'],
	content: ['./src/app.css', './src/**/*.{html,js,svelte,ts}'],
	safelist: ['dark', 'armodo', 'armodo2'],
	theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
		extend: {
			backgroundImage: {
				'gradient-violet': 'lbg-gradient-to-br from-purple-500 to-pink-500',
				'gradient-violet-dark': 'bg-gradient-to-br from-purple-950 to-pink-950'
			},
			colors: {
				'thistle-green': {
					50: 'hsl(60, 33%, 98%)',
					100: 'hsl(60, 30%, 97%)',
					200: 'hsl(60, 17%, 94%)',
					300: 'hsl(60, 22%, 90%)',
					400: 'hsl(60, 33%, 82%)',
					500: 'hsl(60, 33%, 69%)',
					600: 'hsl(60, 29%, 62%)',
					700: 'hsl(60, 12%, 42%)',
					800: 'hsl(60, 12%, 31%)',
					900: 'hsl(60, 12%, 20%)'
				},
				'faded-jade': {
					50: 'hsl(180, 22%, 96%)',
					100: 'hsl(180, 22%, 94%)',
					200: 'hsl(180, 17%, 85%)',
					300: 'hsl(180, 17%, 79%)',
					400: 'hsl(180, 22%, 58%)',
					500: 'hsl(180, 24%, 41%)',
					600: 'hsl(180, 23%, 36%)',
					700: 'hsl(180, 23%, 24%)',
					800: 'hsl(180, 22%, 19%)',
					900: 'hsl(180, 22%, 15%)'
				},
				oregon: {
					50: 'hsl(30, 62%, 97%)',
					100: 'hsl(30, 65%, 93%)',
					200: 'hsl(30, 54%, 85%)',
					300: 'hsl(30, 54%, 75%)',
					400: 'hsl(30, 57%, 53%)',
					500: 'hsl(30, 91%, 34%)',
					600: 'hsl(30, 86%, 29%)',
					700: 'hsl(30, 91%, 20%)',
					800: 'hsl(30, 91%, 14%)',
					900: 'hsl(30, 91%, 10%)'
				},
				gumbo: {
					50: 'hsl(200, 33%, 97%)',
					100: 'hsl(200, 20%, 95%)',
					200: 'hsl(200, 23%, 90%)',
					300: 'hsl(200, 25%, 84%)',
					400: 'hsl(200, 29%, 71%)',
					500: 'hsl(200, 26%, 55%)',
					600: 'hsl(200, 22%, 50%)',
					700: 'hsl(200, 15%, 34%)',
					800: 'hsl(200, 17%, 24%)',
					900: 'hsl(200, 19%, 17%)'
				},
				border: 'hsl(var(--border) / <alpha-value>)',
				input: 'hsl(var(--input) / <alpha-value>)',
				ring: 'hsl(var(--ring) / <alpha-value>)',
				background: 'hsl(var(--background) / <alpha-value>)',
				foreground: 'hsl(var(--foreground) / <alpha-value>)',
				primary: {
					DEFAULT: 'hsl(var(--primary) / <alpha-value>)',
					foreground: 'hsl(var(--primary-foreground) / <alpha-value>)'
				},
				secondary: {
					DEFAULT: 'hsl(var(--secondary) / <alpha-value>)',
					foreground: 'hsl(var(--secondary-foreground) / <alpha-value>)'
				},
				destructive: {
					DEFAULT: 'hsl(var(--destructive) / <alpha-value>)',
					foreground: 'hsl(var(--destructive-foreground) / <alpha-value>)'
				},
				muted: {
					DEFAULT: 'hsl(var(--muted) / <alpha-value>)',
					foreground: 'hsl(var(--muted-foreground) / <alpha-value>)'
				},
				accent: {
					DEFAULT: 'hsl(var(--accent) / <alpha-value>)',
					foreground: 'hsl(var(--accent-foreground) / <alpha-value>)'
				},
				popover: {
					DEFAULT: 'hsl(var(--popover) / <alpha-value>)',
					foreground: 'hsl(var(--popover-foreground) / <alpha-value>)'
				},
				card: {
					DEFAULT: 'hsl(var(--card) / <alpha-value>)',
					foreground: 'hsl(var(--card-foreground) / <alpha-value>)'
				}
			},
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			fontFamily: {
				sans: [...fontFamily.sans]
			}
		}
	}
};

export default config;
