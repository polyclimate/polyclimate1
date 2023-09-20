<script>
	import { base } from '$app/paths';
	import scenarios from '$lib/data/scenarios.json';
</script>

<h3>Scenarios</h3>

{#each scenarios as scenario}
	<a href={`${base}/pathway-demo/${scenario.toLowerCase()}`}>{scenario}</a><br />
{/each}
