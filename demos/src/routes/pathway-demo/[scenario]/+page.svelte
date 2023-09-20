<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { browser } from '$app/environment';
	import {base } from '$app/paths'

	import variables from '$lib/data/variables.json';

	import EmissionsPlot from '$lib/components/EmissionsPlot.svelte';
	import TemperaturePlot from '$lib/components/TemperaturePlot.svelte';

	import 'segmented-control-svelte/lightMode.css'; // Optional, alternatively use darkMode.css or a custom stylesheet
	import { SegmentedControl, Segment } from 'segmented-control-svelte';

	import RangeSlider from 'svelte-range-slider-pips';

	const scenarioMapping = {
		'minus-10': -10,
		'minus-9': -9,
		'minus-8': -8,
		'minus-7': -7,
		'minus-6': -6,
		'minus-5': -5,
		'minus-4': -4,
		'minus-3': -3,
		'minus-2': -2,
		'minus-1': -1,
		persistence: 0,
		'plus-1': 1,
		'plus-2': 2,
		'plus-3': 3
	};

	let scenario = $page.params.scenario;

	let selectedScenario = scenarioMapping[scenario];
	$: scenarioValue = [selectedScenario];

	$: {
		if (scenarioValue[0] < 0) {
			scenario = `minus${scenarioValue[0]}`;
		} else if (scenarioValue[0] > 0) {
			scenario = `plus-${scenarioValue[0]}`;
		} else if (scenarioValue[0] === 0) {
			scenario = 'persistence';
		}
		if (browser) goto(`${base}/pathway-demo/${scenario}`);
	}
	let selectedVariable = 'Emissions|CO2|Energy and Industrial Processes';

	/** @type {import('./$types').PageData} */
	export let data;

	const lowerRanges = ['5.0', '10.0', '16.7', '17.0', '25.0', '33.0'];
	const upperRanges = ['95.0', '90.0', '83.3', '83.0', '75.0', '66.0'];
	let selectedRangeIdx = 0;

	$: variableData = data?.scenario?.filter((i) => i.variable === selectedVariable);
</script>

<div class="wrapper">
	<div class="column">
		<div style="width: 300px">
			<b>Emissions reduction/increase [%]</b>
			<RangeSlider bind:values={scenarioValue} min={-10} max={3} step={1} pips={true} all="label" />
		</div>

		<label for="variables">Variable</label>
		<select bind:value={selectedVariable} name="variables" id="variables">
			{#each variables as variable}
				<option value={variable}>{variable}</option>
			{/each}
		</select>

		<div class="plot">
			<p>
				{selectedVariable}<br />
				<small>Unit: {variableData?.length > 0 && variableData[0].unit}</small>
			</p>
			<EmissionsPlot data={variableData} />
		</div>
	</div>

	<div class="column">
		<div>
			<h4>
				{scenarioValue[0] < 0
					? 'Emissions Reduction: '
					: scenarioValue[0] === 0
					? 'No change in emissions:'
					: 'Emissions Increase:'}
				{scenarioValue}%
			</h4>
		</div>

		<div class="plot">
			Percentile range of FaIR 1.6.2 probabilistic run output:
			<SegmentedControl bind:selectedIndex={selectedRangeIdx}>
				{#each lowerRanges as lower, idx}
					<Segment
						><div class="percentile">{lower}–</div>
						<div class="percentile">{upperRanges[idx]}</div></Segment
					>
				{/each}
			</SegmentedControl>

			<p>
				Surface Temperature (GSAT)<br />
				<small>Unit: {data.results?.length > 0 && data.results[0].unit}</small>
			</p>
			<TemperaturePlot
				data={data.results}
				lower={lowerRanges[selectedRangeIdx]}
				upper={upperRanges[selectedRangeIdx]}
			/>
		</div>
	</div>
</div>

<style>
	.plot {
		width: 420px;
	}
	.wrapper {
		display: grid;
		grid-template-columns: 1fr;
		grid-gap: 20px;
		max-width: 1024px;
	}
	@media (min-width: 768px) {
		.wrapper {
			grid-template-columns: 1fr 1fr;
		}
	}
	.column {
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		padding: 10px;
	}
	.percentile {
		font-size: 0.6rem;
	}
</style>
