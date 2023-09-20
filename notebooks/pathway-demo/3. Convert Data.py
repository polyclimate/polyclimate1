import pathlib

import pyam

root = pathlib.Path(__file__).parent
print(root)

df = pyam.IamDataFrame(root / "data/polyclimate.csv").data
results = pyam.IamDataFrame(root / "data/polyclimate_alloutput.xlsx")

scenarios = df.scenario.unique()

for scenario in scenarios:
    print(scenario)
    sel = df[(df.scenario == scenario)]
    sel[["scenario", "region", "variable", "unit", "year", "value"]].to_json(
        root / f"interactive-demo/static/data/{scenario.lower()}.json", orient="records"
    )
    results.filter(
        scenario=scenario, region="World", variable="*|Surface Temperature (GSAT)*"
    ).data[["scenario", "region", "variable", "unit", "year", "value"]].to_json(
        root / f"interactive-demo/static/data/results-{scenario.lower()}.json",
        orient="records",
    )

df.variable.drop_duplicates().to_json(
    root / "interactive-demo/src/lib/data/variables.json", orient="records"
)
df.scenario.drop_duplicates().to_json(
    root / "interactive-demo/src/lib/data/scenarios.json", orient="records"
)
