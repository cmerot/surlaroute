<script lang="ts">
	import { page } from '$app/stores';
</script>

<h1>{$page.status}</h1>
<p>{$page.error?.message}</p>
<!-- <p>error code: {$page.error?.status}</p> -->
