import typography from "@tailwindcss/typography";
import type { Config } from "tailwindcss";
import tailwindcssAnimate from "tailwindcss-animate";
import { fontFamily } from "tailwindcss/defaultTheme";

const safelist = [
	"dark",
	"nb",
	"vert",
	"marron",
	{
		pattern: /(bg|text)-(bateau|equestre|marche|velo)-(5|4|3)00/,
	},
];

const config: Config = {
	darkMode: ["class"],
	content: ["./src/**/*.{html,js,svelte,ts}"],
	safelist,
	theme: {
		container: {
			center: true,
			padding: "2rem",
			screens: {
				"2xl": "1400px",
			},
		},
		extend: {
			backgroundImage: {
				"gradient-violet": "lbg-gradient-to-br from-purple-500 to-pink-500",
				"gradient-violet-dark": "bg-gradient-to-br from-purple-950 to-pink-950",
			},
			colors: {
				border: "hsl(var(--border) / <alpha-value>)",
				input: "hsl(var(--input) / <alpha-value>)",
				ring: "hsl(var(--ring) / <alpha-value>)",
				background: "hsl(var(--background) / <alpha-value>)",
				foreground: "hsl(var(--foreground) / <alpha-value>)",
				primary: {
					DEFAULT: "hsl(var(--primary) / <alpha-value>)",
					foreground: "hsl(var(--primary-foreground) / <alpha-value>)",
				},
				secondary: {
					DEFAULT: "hsl(var(--secondary) / <alpha-value>)",
					foreground: "hsl(var(--secondary-foreground) / <alpha-value>)",
				},
				destructive: {
					DEFAULT: "hsl(var(--destructive) / <alpha-value>)",
					foreground: "hsl(var(--destructive-foreground) / <alpha-value>)",
				},
				muted: {
					DEFAULT: "hsl(var(--muted) / <alpha-value>)",
					foreground: "hsl(var(--muted-foreground) / <alpha-value>)",
				},
				accent: {
					DEFAULT: "hsl(var(--accent) / <alpha-value>)",
					foreground: "hsl(var(--accent-foreground) / <alpha-value>)",
				},
				popover: {
					DEFAULT: "hsl(var(--popover) / <alpha-value>)",
					foreground: "hsl(var(--popover-foreground) / <alpha-value>)",
				},
				card: {
					DEFAULT: "hsl(var(--card) / <alpha-value>)",
					foreground: "hsl(var(--card-foreground) / <alpha-value>)",
				},
				sidebar: {
					DEFAULT: "hsl(var(--sidebar-background))",
					foreground: "hsl(var(--sidebar-foreground))",
					primary: "hsl(var(--sidebar-primary))",
					"primary-foreground": "hsl(var(--sidebar-primary-foreground))",
					accent: "hsl(var(--sidebar-accent))",
					"accent-foreground": "hsl(var(--sidebar-accent-foreground))",
					border: "hsl(var(--sidebar-border))",
					ring: "hsl(var(--sidebar-ring))",
				},
				"thistle-green": {
					50: "hsl(60, 33%, 98%)",
					100: "hsl(60, 30%, 97%)",
					200: "hsl(60, 17%, 94%)",
					300: "hsl(60, 22%, 90%)",
					400: "hsl(60, 33%, 82%)",
					500: "hsl(60, 33%, 69%)",
					600: "hsl(60, 29%, 62%)",
					700: "hsl(60, 12%, 42%)",
					800: "hsl(60, 12%, 31%)",
					900: "hsl(60, 12%, 20%)",
				},
				"faded-jade": {
					50: "hsl(180, 22%, 96%)",
					100: "hsl(180, 22%, 94%)",
					200: "hsl(180, 17%, 85%)",
					300: "hsl(180, 17%, 79%)",
					400: "hsl(180, 22%, 58%)",
					500: "hsl(180, 24%, 41%)",
					600: "hsl(180, 23%, 36%)",
					700: "hsl(180, 23%, 24%)",
					800: "hsl(180, 22%, 19%)",
					900: "hsl(180, 22%, 15%)",
				},
				oregon: {
					50: "hsl(30, 62%, 97%)",
					100: "hsl(30, 65%, 93%)",
					200: "hsl(30, 54%, 85%)",
					300: "hsl(30, 54%, 75%)",
					400: "hsl(30, 57%, 53%)",
					500: "hsl(30, 91%, 34%)",
					600: "hsl(30, 86%, 29%)",
					700: "hsl(30, 91%, 20%)",
					800: "hsl(30, 91%, 14%)",
					900: "hsl(30, 91%, 10%)",
				},
				gumbo: {
					50: "hsl(200, 33%, 97%)",
					100: "hsl(200, 20%, 95%)",
					200: "hsl(200, 23%, 90%)",
					300: "hsl(200, 25%, 84%)",
					400: "hsl(200, 29%, 71%)",
					500: "hsl(200, 26%, 55%)",
					600: "hsl(200, 22%, 50%)",
					700: "hsl(200, 15%, 34%)",
					800: "hsl(200, 17%, 24%)",
					900: "hsl(200, 19%, 17%)",
				},
				velo: {
					500: "hsl(278, 36%, 82%)",
					400: "hsl(278, 38%, 89%)",
					300: "hsl(274, 58%, 93%)",
				},
				equestre: {
					500: "hsl(17, 16%, 53%)",
					400: "hsl(23, 17%, 65%)",
					300: "hsl(23, 20%, 76%)",
				},
				bateau: {
					500: "hsl(207, 39%, 70%)",
					400: "hsl(210, 41%, 79%)",
					300: "hsl(220, 50%, 88%)",
				},
				marche: {
					500: "hsl(52, 44%, 60%)",
					400: "hsl(51, 50%, 71%)",
					300: "hsl(48, 49%, 84%)",
				},
				couleur: {
					dark: "#7b6191",
					bg: "#b696c6",
					fg: "#fff",
				},
				nb: {
					bg: "#fff",
					fg: "#000",
				},
				neg: {
					bg: "#000",
					fg: "#fff",
				},
				gris: {
					bg: "#9d9d9c",
					fg: "#575756",
				},
			},
			borderRadius: {
				xl: "calc(var(--radius) + 4px)",
				lg: "var(--radius)",
				md: "calc(var(--radius) - 2px)",
				sm: "calc(var(--radius) - 4px)",
			},
			fontFamily: {
				logo: ["Marker Aid", "marker-aid", ...fontFamily.sans],
				sans: ["Roboto", ...fontFamily.sans],
			},
			keyframes: {
				"accordion-down": {
					from: { height: "0" },
					to: {
						height: "var(--bits-accordion-content-height)",
					},
				},
				"accordion-up": {
					from: {
						height: "var(--bits-accordion-content-height)",
					},
					to: { height: "0" },
				},
				"caret-blink": {
					"0%,70%,100%": { opacity: "1" },
					"20%,50%": { opacity: "0" },
				},
			},
			animation: {
				"accordion-down": "accordion-down 0.2s ease-out",
				"accordion-up": "accordion-up 0.2s ease-out",
				"caret-blink": "caret-blink 1.25s ease-out infinite",
			},
		},
	},
	plugins: [tailwindcssAnimate, typography],
};

export default config;
