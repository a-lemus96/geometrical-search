import geopandas as gpd
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Tuple

import tree as kd
import vptree as vpt

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

colors = ['red', 'orange', 'brown', 'green', 'cyan', 'magenta', 'black', 'gray']

def draw_subtree(node: kd.TreeNode, s: int, color: str) -> None:
    width = 8 - s
    if node.left != None:
        draw_subtree(node.left, s + 1, color=colors[(s + 1) % 7])
    # draw current node as a line segment
    if width > 0:
        if node.split_x == True:
            plt.plot(2 * [node.x], [max(-6, node.ymin), min(node.ymax, 5)],
                     linewidth=width, color=color)
        else:
            plt.plot([max(-5, node.xmin), min(node.xmax, 5)], 2 * [node.y],
                     linewidth=width, color=color)

    if node.right != None:
        draw_subtree(node.right, s + 1, color=colors[(s + 1) % 7])

def draw(tree: kd.Tree) -> None:
    draw_subtree(tree.root, 0, colors[0])


def plot_random(n: int = 5) -> List[np.ndarray]:
    """Plots random 2d-points sampled from a uniform distribution.
    ----------------------------------------------------------------------------
    Args:
        n: number of random points
    Returns:
        points: List of two (n,)-shape arrays containing pairs of coords"""
    xs = np.random.uniform(low=-4, high=4, size=n)            
    ys = np.random.uniform(low=-6, high=5, size=n)

    # plot points
    plt.scatter(xs, ys, color='green', linewidth=0.05)

    return [xs, ys]

# read data
df = pd.read_json('data/station_information.json')
station_pos = df[['lon','lat']].values.reshape(-1, 2)

# compute average
lon_mean = np.average(station_pos[:, 0])
lat_mean = np.average(station_pos[:, 1])

# convert coords into x,y position
locs_bike = np.apply_along_axis(latlon_to_global, 1, station_pos)

# plot station positions
plt.figure()
plt.scatter(locs_bike[:, 0], locs_bike[:, 1], linewidth=0.05)
plt.gca().set_aspect('equal', adjustable='box')
plt.legend('Ecobici Stations')
plt.savefig('out/station_locations.png')

# plot 2d-tree
plt.figure()
# create 2d-tree using ecobike data
tree = kd.Tree(locs_bike[:, 0], locs_bike[:, 1])
plt.scatter(locs_bike[:, 0], locs_bike[:, 1], linewidth=0.05)
plt.gca().set_aspect('equal', adjustable='box')
draw(tree)
plt.savefig('out/tree.png')

# plot query points and their nearest neighbors
plt.figure()
plt.scatter(locs_bike[:, 0], locs_bike[:, 1], linewidth=0.05)
plt.gca().set_aspect('equal', adjustable='box')
points = plot_random(n=30)
# compute and plot nearest neighbor for all random points
nearest_neighbors = []
for query in zip(points[0], points[1]):
    _, nearest = tree.nearest_neighbor(query, tree.root)
    # plot node and draw a line to the query point
    plt.scatter([nearest.x], [nearest.y], color='red', linewidth=0.05)
    plt.plot([nearest.x, query[0]], [nearest.y, query[1]], color='k')

plt.savefig('out/nearest.png')

# plot query points and their nearest neighbors using VpTree
plt.figure()
# create vp-tree using ecobike data
locs = []
for coord in locs_bike:
    locs.append(coord)
vptree = vpt.VpTree(locs)

plt.scatter(locs_bike[:, 0], locs_bike[:, 1], linewidth=0.05)
plt.gca().set_aspect('equal', adjustable='box')
points = plot_random(n=30)
# compute and plot nearest neighbor for all random points
nearest_neighbors = []
for query in zip(points[0], points[1]):
    nearest, _ = vptree.nearest_neighbor(query)
    # plot node and draw a line to the query point
    plt.scatter([nearest.vp[0]], [nearest.vp[1]], color='red', linewidth=0.05)
    plt.plot([nearest.vp[0], query[0]], [nearest.vp[1], query[1]], color='k')

plt.savefig('out/nearest_vpt.png')
