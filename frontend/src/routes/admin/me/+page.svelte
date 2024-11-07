<script lang="ts">
	import { Avatar, AvatarFallback } from '$lib/components/ui/avatar';
	import { Badge } from '$lib/components/ui/badge';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Label } from '$lib/components/ui/label';
	import { addCrumb } from '$lib/utils.js';
	import { User } from 'lucide-svelte';

	addCrumb('/admin/me', 'Mon profil');

	let { data } = $props();
	const { email, full_name, is_active, is_superuser, id } = data;
</script>

<Card class="mx-auto mt-8 max-w-md">
	<CardHeader>
		<CardTitle class="text-center text-2xl font-bold">User Profile</CardTitle>
	</CardHeader>
	<CardContent>
		<div class="flex flex-col items-center space-y-4">
			<Avatar class="h-24 w-24">
				<AvatarFallback><User class="h-12 w-12" /></AvatarFallback>
			</Avatar>

			<div class="text-center">
				<h2 class="text-xl font-semibold">{full_name}</h2>
				<p class="text-sm text-muted-foreground">{email}</p>
			</div>

			<div class="flex space-x-2">
				<Badge variant={is_active ? 'default' : 'secondary'}>
					{is_active ? 'Active' : 'Inactive'}
				</Badge>
				{#if is_superuser}
					<Badge variant="default">Superuser</Badge>
				{/if}
			</div>

			<div class="w-full space-y-2">
				<div>
					<Label for="user-id">User ID</Label>
					<p id="user-id" class="text-sm font-medium">{id}</p>
				</div>
				<div>
					<Label for="user-email">Email</Label>
					<p id="user-email" class="text-sm font-medium">{email}</p>
				</div>
				<div>
					<Label for="user-name">Full Name</Label>
					<p id="user-name" class="text-sm font-medium">{full_name}</p>
				</div>
			</div>
		</div>
	</CardContent>
</Card>
