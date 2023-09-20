import logging

LOGGING_LEVEL = logging.INFO

LOGGER = logging.getLogger("pipeline")
LOGGER.setLevel(LOGGING_LEVEL)
# have to set root logger too to get messages to come through
logging.getLogger().setLevel(LOGGING_LEVEL)

logFormatter = logging.Formatter(
    "%(asctime)s %(name)s %(threadName)s - %(levelname)s:  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
stdoutHandler = logging.StreamHandler()
stdoutHandler.setFormatter(logFormatter)

logging.getLogger().addHandler(stdoutHandler)


import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import pathlib

root = pathlib.Path(__file__).parent
print(root)

import pooch
import pyam
from climate_assessment.cli import run_workflow

# ### Download FaIR configuration

fair_slim_filename = "fair-1.6.2-wg3-params-slim.json"
fair_common_filename = "fair-1.6.2-wg3-params-common.json"


fair_slim_url = (
    "https://zenodo.org/record/6601980/files/fair-1.6.2-wg3-params-slim.json?download=1"
)
fair_slim_hash = "c071ca619c0ae37a6abdeb79c0cece7b"

pooch.retrieve(
    url=fair_slim_url,
    known_hash=f"md5:{fair_slim_hash}",
    path=root / "data",
    fname=root / "data" / fair_slim_filename,
)


fair_common_url = "https://zenodo.org/record/6601980/files/fair-1.6.2-wg3-params-common.json?download=1"
fair_common_hash = "42ccaffcd3dea88edfca77da0cd5789b"

pooch.retrieve(
    url=fair_common_url,
    known_hash=f"md5:{fair_common_hash}",
    path=root / "data",
    fname=root / "data" / fair_common_filename,
)

model = "fair"
model_version = "1.6.2"
fair_extra_config = root / "data" / fair_common_filename
probabilistic_file = root / "data" / fair_slim_filename

# Use fewer (e.g. 10) if you just want to do a test run but note that this breaks
# the stats of the probabilistic ensemble
num_cfgs = 2237
# Set to True if you're not using the full FaIR ensemble
test_run = False
# How many scenarios do you want to run in one go?
scenario_batch_size = 2

outdir = str(root / "data")

input_emissions_file = str(root / "data" / "polyclimate.csv")

infilling_database_file = str(
    root
    / "data"
    / "1652361598937-ar6_emissions_vetted_infillerdatabase_10.5281-zenodo.6390768.csv"
)


run_workflow(
    input_emissions_file,
    outdir,
    model=model,
    model_version=model_version,
    probabilistic_file=probabilistic_file,
    fair_extra_config=fair_extra_config,
    num_cfgs=num_cfgs,
    infilling_database=infilling_database_file,
    scenario_batch_size=scenario_batch_size,
    harmonize=True,
)

output = pyam.IamDataFrame(root / "data" / "polyclimate_alloutput.xlsx")
print(output)
