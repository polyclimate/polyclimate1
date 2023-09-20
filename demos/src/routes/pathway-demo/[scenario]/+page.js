import {base} from '$app/paths'

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
	const [scenarioReq, resultsReq] = await Promise.all([
		fetch(`${base}/data/${params.scenario}.json`),
		fetch(`${base}/data/results-${params.scenario}.json`)
	]);

	if (scenarioReq.ok && resultsReq.ok) {
		const scenario = await scenarioReq.json();
		const results = await resultsReq.json();

		return { scenario, results };
	}
}
