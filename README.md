# Geometrical Search
This repository contains two implementations of the nearest neighbor problem in 2d: using a variance-splitting-based 2d-tree and a vantage point tree. It tests the implementations using the EcoBici station locations in Mexico City, the data is located in `data` folder under the `station_information.jason` filename. To reproduce results, please run `python ecobici.py` and head out to `out` folder. The first result is `station_locations.png`, a simple plot of the $xy$ coordinates of all bike stations that should look like the following image:

![image](https://user-images.githubusercontent.com/95151624/233959851-85cbbea2-8f34-46a0-9def-c1ddefeb4e66.png)

### Nearest neighbor (NN) using 2d-trees
---
We use a variance-based 2d-tree such that if the data variance along $x$ is superior to the data variance along $y$, then we split along $y$. Otherwise,
we split along $y$.  Tree implementation along with its nearest neighbor method are coded in `tree.py`. The output file `out/tree.png` shows a drawing of the variance-based 2d-tree.

![image](https://user-images.githubusercontent.com/95151624/233960788-e2951880-5fb9-44c9-b16a-d97a4d32da9d.png)

Next, you can find `out/nearest.png` where I have used 30 random query points (in green) and computed their nearest neighbors. I drawed joining lines in black for more clarity.

![image](https://user-images.githubusercontent.com/95151624/233961406-484cdb14-0425-4c9e-b1ec-882671a15a26.png)

### Nearest neighbor (NN) using vantage point trees (VP-trees)
---
Next, VP-tree implementation along with its nearest_neighbor method may be found in `vptree.py`. You can find `out/nearest_vpt.png` where I performed the same process as with 2d-trees to test NN method.

![image](https://user-images.githubusercontent.com/95151624/233962219-93271081-8e47-4b1f-8a76-a1ad0d82f48a.png)

### Changing VP-Trees definition
---
Suppose that we modify a bit the VP-tree definition and that instead of partitioning the data points under each node into two subsets (closest/farthest to the vantage point), we create $m$ subsets by sorting the distances in increasing order and partitioning the points according to their distance to the vantage point (VP), defining for this purpose $m − 1$ radii corresponding to these $m$ blocks of data.

**Changing the search algorithm**: The sorting and splitting process in terms of the distance to the soon-to-be subtree node yields a $(m-1)$-ary tree. Each node has $m - 1$ space-partitioning nodes associated with it. Moreover, the $m-1$ partitioning children of a particular node define $m-1$ concentric circular splitting boundaries. Thus, we can associate each node in the tree with a region $R$ of the form:

$$
      R_i:\quad \set{v:\quad d(v, x) \in [r_i,\quad r_i+1)}\quad\quad i \in \set{0, 1, 2, \dots, m-1}
$$

Where $x$ is the absolute root node. Furthermore, we have that $r_0$ and $r_m$ are the limiting boundaries for the subtree. In order to search for a point within the tree, we must proceed with a recursive approach. At each level, based on query node coordinates and node region boundaries, we must check to which of the $m$ regions the point belongs. By construction of the tree, it must fit in exactly one of them. We continue recursively until we reach a node whose children are `None` and either we return `False` if the search was unsuccesful, `True` otherwise. If we find a match along the searching path before reaching the previous state, we return `True`.

**Complexity Analysis**: 
