import math
import numpy as np
from typing import List

def distance(point1: List[float], point2: List[float]) -> float:
    return math.sqrt((point1[1] - point2[1])**2 + (point1[0] - point2[0])**2)

# Adaptation from VP-Tree implementation, by Steve Hanov. (steve.hanov@gmail.com)

# Node class
class VpTreeNode:
    def __init__(self, point):
        self.vp = point
        self.left = None
        self.right = None
        self.mu = 0

    def __str__(self):
        return f"(vp={self.vp}, mu={self.mu})"


# VPTree Class
class VpTree:
    def __init__(self, datapoints):
        self._datapoints = datapoints
        self._root = self.__build(0, len(self._datapoints))

    def __build(self, low_idx, up_idx):
        # terminal case
        if up_idx == low_idx:
            return None

        # terminal case with one node
        if up_idx - low_idx == 1:
            node = VpTreeNode(self._datapoints[low_idx])
            return node

        # if previous conditions are not met, then there are at least two data
        root_i = np.random.randint(low_idx, up_idx) # choose rand index for root
        # swap corresponding element with starting element
        tmp = self._datapoints[root_i], self._datapoints[low_idx]
        self._datapoints[low_idx], self._datapoints[root_i] = tmp

        # compute all distances to subtree's root node
        dists = [distance(p, self._datapoints[low_idx])
                for p in self._datapoints[low_idx:up_idx]]
        mid = len(dists) // 2 # distances' middle element
        # move all elements lower to mid element to left and higher to the right
        idx = np.argpartition(dists, mid)
        zero = np.argwhere(idx == 0)[0][0] # track position of zero idx
        # swap it to the leftmost position
        idx[zero] = idx[0]
        idx[0] = 0

        # partially sort data based on their distance to low_idx element
        tmp = [self._datapoints[low_idx + i] for i in idx]
        self._datapoints[low_idx:up_idx] = tmp
        
        # create subtree root node
        node = VpTreeNode(self._datapoints[low_idx])
        node.mu = distance(self._datapoints[low_idx],
                           self._datapoints[low_idx + mid])

        # recursive call for left and right child nodes
        node.left = self.__build(low_idx + 1, low_idx + mid + 1)
        node.right = self.__build(low_idx + mid + 1, up_idx)

        return node

    def __nearest_neighbor(
              self, 
              query, 
              node, 
              tau: float = math.inf, 
              nn: VpTreeNode = None) -> VpTreeNode:
        """"""
        if node != None:
            d = distance(query, node.vp)
            if nn == None: # special case at initialization
                tau = d
                nn = node
                # explore inner region
                nl, tl = self.__nearest_neighbor(query, node.left, 
                                                 tau=tau, nn=nn)
                if tl < tau:
                    tau = tl 
                    nn = nl
                # explore outter region
                nr, tr = self.__nearest_neighbor(query, node.right, 
                                                 tau=tau, nn=nn)
                if tr < tau:
                    tau = tr
                    nn = nr
            else: # second iteration onward
                tau = d
                nn = node
                if tau + node.mu < d: # prune inner tree
                    nr, tr = self.__nearest_neighbor(query, node.right,
                                                     tau=d, nn=nn)
                    if tr < tau:
                        tau = tr
                        nn = nr
                elif tau < node.mu and d < node.mu - tau: # prune outter tree
                    nl, tl = self.__nearest_neighbor(query, node.left,
                                                     tau=d, nn=nn)
                    if tl < tau:
                        tau = tl
                        nn = nl
                elif node.mu - tau < d and d < node.mu + tau: # check both trees
                    # explore inner region
                    nl, tl = self.__nearest_neighbor(query, node.left, 
                                                     tau=d, nn=nn)
                    if tl < tau:
                        tau = tl 
                        nn = nl
                    # explore outter region
                    nr, tr = self.__nearest_neighbor(query, node.right, 
                                                     tau=tau, nn=nn)
                    if tr < tau:
                        tau = tr
                        nn = nr
        return nn, tau

    def nearest_neighbor(self, query) -> VpTreeNode:
        return self.__nearest_neighbor(query, self._root)

    def print(self):
        self.__print_subtree(self._root)

    def __print_subtree(self, node):
        if node.left != None:
            self.__print_subtree(node.left)
        print(node)
        if node.right != None:
            self.__print_subtree(node.right)
