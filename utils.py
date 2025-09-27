import fastf1
from fastf1 import plotting
import matplotlib

def setup():
    fastf1.Cache.enable_cache('cache')  # create a local cache folder
    plotting.setup_mpl(misc_mpl_mods=False)  # optional: improve colors
    matplotlib.rcParams['figure.figsize'] = [10, 6]
