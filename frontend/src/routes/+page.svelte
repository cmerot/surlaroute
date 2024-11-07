<script>
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { CircleAlert } from 'lucide-svelte';
</script>

<div
	class="flex min-h-screen items-center justify-center bg-gradient-to-r from-purple-400 via-pink-500 to-red-500"
>
	<Card class="w-full max-w-md bg-white/90 shadow-xl backdrop-blur-sm">
		<CardHeader>
			<CardTitle class="text-center text-4xl font-bold text-gray-800">Sur la Route</CardTitle>
		</CardHeader>
		<CardContent>
			<div class="flex flex-col items-center space-y-4">
				<CircleAlert class="h-16 w-16 text-yellow-500" />
				<p class="text-center text-xl text-gray-700">
					Oops! Our site is currently under construction. We're working hard to bring you something
					amazing!
				</p>
			</div>
		</CardContent>
		<CardFooter class="flex justify-center">
			<Button
				href="/admin"
				class="bg-gradient-to-r from-blue-500 to-indigo-600 font-semibold text-white hover:from-blue-600 hover:to-indigo-700"
				>Visit Admin</Button
			>
		</CardFooter>
	</Card>
</div>
