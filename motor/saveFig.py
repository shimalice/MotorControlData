# Common imports
import os

# To plot pretty figures
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# Where to save the figures
def _make_path(CLUSTER_NAME='fig'):
    PROJECT_ROOT_DIR = "."
    IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CLUSTER_NAME)
    return IMAGES_PATH

def save_fig(fig_dir, fig_id, fig_extension="png", resolution=300):
    IMAGES_PATH = _make_path(fig_dir)
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    plt.savefig(path, format=fig_extension, dpi=resolution)
