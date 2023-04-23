import geopandas as gpd
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Tuple

import tree as kd

def latlon_to_global(coords: np.ndarray) -> Tuple[float]:
    """Converts latitude and longitude coordinates to local x, y positions
    (around the mean). This is a first order approximation.
    ----------------------------------------------------------------------------
    Args:
        coords: (2,)-shape numpy array containint latitude/longitude coords
    Retuns:
        x, y: x, y positions
    """
    rad = 6371.0 # earth radius
    dlon = math.pi * (coords[0] - lon_mean) / 180.0
    dlat = math.pi * (coords[1] - lat_mean) / 180.0
    x = rad * dlon * math.cos(math.pi * lat_mean / 180.0)
    y = rad * dlat

    return x, y

def draw_subtree(node: kd.TreeNode, s: int) -> None:
    if node.left != None:
        draw_subtree(node.left, s + 1)
    # draw current node as a line segment
    width = 8 - s
    if width > 0:
        if node.split_x == True:
            plt.plot(2 * [node.x], [max(-6, node.ymin), min(node.ymax, 5)],
                     linewidth=width)
        else:
            plt.plot([max(-5, node.xmin), min(node.xmax, 5)], 2 * [node.y],
                     linewidth=width)

    if node.right != None:
        draw_subtree(node.right, s + 1)

def draw(tree: kd.Tree) -> None:
    draw_subtree(tree.root, 0)
                

# read data
df = pd.read_json('data/station_information.json')
station_pos = df[['lon','lat']].values.reshape(-1, 2)

# compute average
lon_mean = np.average(station_pos[:, 0])
lat_mean = np.average(station_pos[:, 1])

# convert coords into x,y position
locs_bike = np.apply_along_axis(latlon_to_global, 1, station_pos)

# plot station positions
plt.scatter(locs_bike[:, 0], locs_bike[:, 1])
plt.gca().set_aspect('equal', adjustable='box')
plt.legend('Ecobici Stations')
plt.savefig('out/station_locations.png')

# create 2d-tree using ecobike data
tree = kd.Tree(locs_bike[:, 0], locs_bike[:, 1])
#plt.gca().set_aspect('equal', adjustable='box')
draw(tree)
plt.savefig('out/tree.png')
