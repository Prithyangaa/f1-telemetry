import fastf1
from fastf1 import plotting
import matplotlib

def setup():
    if not os.path.exists("cache"):
        os.makedirs("cache")
    fastf1.Cache.enable_cache('cache')  # create a local cache folder
    plotting.setup_mpl(misc_mpl_mods=False) 
    matplotlib.rcParams['figure.figsize'] = [10, 6]
