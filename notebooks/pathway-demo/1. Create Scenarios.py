import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import pathlib

import pandas as pd
import pyam

root = pathlib.Path(__file__).parent

hist_df = pd.read_csv(
    "https://github.com/iiasa/climate-assessment/raw/485f3d24fc646ad8d77c65ac5e787a27dc79db04/src/climate_assessment/harmonization/history_ar6.csv"
)

hist = pyam.IamDataFrame(hist_df)

igcc = pd.read_csv(
    "https://github.com/ClimateIndicator/GHG-Emissions-Assessment/raw/edd48a54187b8ee6f16d6c8a5735970cd1499bce/results/ghg_emissions_co2e.csv"
)

igcc = igcc.drop("units", axis=1)
igcc = igcc.set_index("year")

change_rate = igcc.pct_change()
change_rate.tail()

mapping = {
    "AR6 climate diagnostics|Emissions|CO2|Energy and Industrial Processes|Unharmonized": "CO2-FFI",
    "AR6 climate diagnostics|Emissions|CO2|AFOLU|Unharmonized": "CO2-LULUCF",
    "AR6 climate diagnostics|Emissions|CH4|Unharmonized": "CH4",
    "AR6 climate diagnostics|Emissions|N2O|Unharmonized": "N2O",
    "AR6 climate diagnostics|Emissions|F-Gases|Unharmonized": "F-gases",
}

for year in range(2016, 2022):
    hist_df[str(year)] = None
    for k, v in mapping.items():
        print(k)
        value = hist_df[hist_df.Variable == k][str(year - 1)].values[0]
        idx = hist_df[hist_df.Variable == k][str(year)].index.values[0]
        hist_df.loc[idx, str(year)] = value + (value * change_rate[v][year])


persistence = hist_df.dropna().copy()

persistence.Model = "Polyclimate"
persistence.Scenario = "Persistence"

for i in range(2022, 2101, 1):
    persistence[str(i)] = persistence[persistence.columns[-1]]

for i in range(1750, 2010, 1):
    persistence = persistence.drop(str(i), axis=1)

# -10% to -1% each year from 2022.

reduction_scenarios = []
for reduction in range(10, 0, -1):
    minus = hist_df.dropna().copy()

    minus.Model = "Polyclimate"
    minus.Scenario = f"Minus-{reduction}"

    for i in range(1750, 2010, 1):
        minus = minus.drop(str(i), axis=1)

    for i in range(2022, 2101, 1):
        minus[str(i)] = (
            minus[minus.columns[-1]] - (reduction / 100) * minus[minus.columns[-1]]
        )

    reduction_scenarios.append(minus)


# 1% to 3s% increase every year from 2022.


increase_scenarios = []
for increase in [1, 2, 3]:
    plus = hist_df.dropna().copy()

    plus.Model = "Polyclimate"
    plus.Scenario = f"Plus-{increase}"

    for i in range(2022, 2101, 1):
        plus[str(i)] = (
            plus[plus.columns[-1]] + (increase / 100) * plus[plus.columns[-1]]
        )

    for i in range(1750, 2010, 1):
        plus = plus.drop(str(i), axis=1)

    increase_scenarios.append(plus)


df = pd.concat([persistence] + reduction_scenarios + increase_scenarios)

df.Variable = df.Variable.apply(
    lambda x: x.replace("AR6 climate diagnostics|", "").replace("|Unharmonized", "")
)
df.to_csv(root / "data/polyclimate.csv", index=False)
