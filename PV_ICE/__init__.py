try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    # for python < 3.8 (remove when dropping 3.7 support)
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = "0+unknown"

from PV_ICE.main import Simulation, Scenario, Material, weibull_params, weibull_cdf, calculateLCA, weibull_cdf_vis
from PV_ICE.main import sens_StageImprovement, sens_StageEfficiency
