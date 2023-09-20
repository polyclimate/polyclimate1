/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
	const [scenarioReq, resultsReq] = await Promise.all([
		fetch(`/data/${params.scenario}.json`),
		fetch(`/data/results-${params.scenario}.json`)
	]);

	if (scenarioReq.ok && resultsReq.ok) {
		const scenario = await scenarioReq.json();
		const results = await resultsReq.json();

		return { scenario, results };
	}
}
