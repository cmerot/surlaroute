<script>
import { enhance } from "$app/forms";
</script>

<form action="/logout" method="post" use:enhance>
	<button type="submit">Logout</button>
</form>
