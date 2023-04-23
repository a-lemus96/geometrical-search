import math
import numpy as np
from typing import List, Tuple


# Node Class
class TreeNode:
    def __init__(
            self,
            x: float,
            y: float,
            split_x: bool = True):
        """Constructor method. Builds a 2d-tree node using spatial input coords 
        and splitting direction.
        -----------------------------------------------------------------------
        Args:
            x: x-coordinate
            y: y-coordinate
            split_x: splitting direction. x if True, y otherwise"""
        # spatial point coords
        self.x = x
        self.y = y
        # rectangular region defined by this node
        self.xmin, self.xmax = -math.inf, math.inf
        self.ymin, self.ymax = -math.inf, math.inf
        # splitting direction
        self.split_x = split_x
        # left and right children
        self.left, self.right = None, None

    def __str__(self) -> str:
        """2d-tree node string representation.
        ------------------------------------------------------------------------
        """
        split = 'x' if self.split_x == True else 'y'
        return f"[(x={str(self.x)}, y={str(self.y)}), split_dir={split}]"


# 2d-Tree class
class Tree:
    def __init__(
            self, 
            xs: List[float], 
            ys: List[float]):
        """Constructor method. Builds a variance dependent 2d-tree using list of 
        spatial input coords.
        -----------------------------------------------------------------------
        Args:
            xs: list of x-coordinates
            ys: list of y-coordinates"""
        # compute indices that would sort xs and ys
        ix_sort, iy_sort = np.argsort(xs), np.argsort(ys)
        # compute variances along xs and ys
        x_var, y_var = np.var(xs), np.var(ys)
        # splitting rule
        split_x = True if x_var > y_var else False
        
        # build tree recursively
        self.root = self.__build_tree(xs, ys, ix_sort, iy_sort, split_x)

    def print(self):
        """Printing method starting at tree's root.
        ------------------------------------------------------------------------
        """
        self.__print_subtree(self.root)

    def __print_subtree(self, node: TreeNode):
        """Recursive tree printing method. Visits subtree defined by node arg
        in order and prints nodes in order as well.
        ------------------------------------------------------------------------
        Args:
            node: root of the subtree to print"""
        if node.left != None:
            self.__print_subtree(node.left) # explore left subtree

        print(node) # print node after exploring left subtree

        if node.right != None:
            self.__print_subtree(node.right) # explore right subtree

    def __select(self, isorted: List[int], isecond: List[int]) -> List[int]:
        """Given an array of indices, select from a second array those that
        match with any of the elements of the first array. From the selected
        items, it preserves the ordering in the second array.
        ------------------------------------------------------------------------
        Args:
            isorted: array of indices that would sort an array
            isecond: array of indices that would sort another array
        Returns:
            io: array of indices in isecond that are contained in isorted, order
                is preserved"""
        io = np.array([]).astype(int)
        # iterate along second array of indices (non-splitting direction)
        for i in isecond:
            r = (isorted == i) # compare isorted elements to i
            if r.any() == True: # element is present in isorted
                io = np.append(io, i)

        return io

    def __get_bounds(
            self, 
            node: TreeNode, 
            parent: TreeNode) -> Tuple[float]:
        """Computes node region's boundaries based on parent splitting dir.
        ------------------------------------------------------------------------
        Args:
            node: 2d-tree node
            parent: parent node
        Returns:
            (4,)-tuple containing rectangular boundaries"""
        xmin, xmax = parent.xmin, parent.xmax
        ymin, ymax = parent.ymin, parent.ymax

        if parent.split_x == True: # parent splits along x
            # check if parent is to the left or right of node
            if parent.x <= node.x:
                xmin = parent.x
            else:
                xmax = parent.x

        else: # parent splits along y
            if parent.y <= node.y:
                ymin = parent.y
            else:
                ymax = parent.y

        return xmin, xmax, ymin, ymax

    def __build_tree(
            self,
            xs: List[float],
            ys: List[float],
            ix: List[int],
            iy: List[int],
            split_x: bool = None,
            parent = None) -> TreeNode:
        """Recursive building method. Builds a 2d-tree for a list of points.
        Uses variance rule for determining splitting direction of child nodes.
        ------------------------------------------------------------------------
        Args:
            xs: list of x-coordinates
            ys: list of y-coordinates
            ix: list of indices that define xs sorting
            iy: list of indices that define ys sorting
            split_x: splitting direction. True if x and False if y
            parent: parent node"""
        size = ix.shape[0] # number of nodes
        mid = size // 2 # middle index
        
        if split_x: # split along x-axis
            # use middle node along x-axis to partition space
            node = TreeNode(xs[ix[mid]], ys[ix[mid]], True)
            if parent != None:
                # compute region's boundaries
                bounds = self.__get_bounds(node, parent)
                node.xmin, node.xmax = bounds[:2]
                node.ymin, node.ymax = bounds[2:]
                
            if mid > 0:
                # select iy elements corresponding to ix[:mid]
                sub_iy = self.__select(ix[:mid], iy)
                # compute splitting axis based on variance rule
                x_var, y_var = np.var(xs[ix[:mid]]), np.var(ys[ix[:mid]])
                split_x = True if x_var > y_var else False
                # build left-subtree
                node.left = self.__build_tree(xs, ys, ix[:mid], sub_iy,
                                              split_x, node)

            if mid + 1 < size:
                sub_iy = self.__select(ix[mid+1:], iy)
                x_var, y_var = np.var(xs[ix[mid+1:]]), np.var(ys[ix[mid+1:]])
                split_x = True if x_var > y_var else False
                # build right-subtree
                node.right = self.__build_tree(xs, ys, ix[mid+1:], sub_iy,
                                              split_x, node)

        else: # split along y-axis
            node = TreeNode(xs[iy[mid]], ys[iy[mid]], False)
            if parent != None:
                bounds = self.__get_bounds(node, parent)
                node.xmin, node.xmax = bounds[:2]
                node.ymin, node.ymax = bounds[2:]

            if mid > 0:
                # select ix elements corresponding to iy[:mid]
                sub_ix = self.__select(iy[:mid], ix)
                x_var, y_var = np.var(xs[iy[:mid]]), np.var(ys[iy[:mid]])
                split_x = True if x_var > y_var else False
                # build left-subtree
                node.left = self.__build_tree(xs, ys, sub_ix, iy[:mid],
                                              split_x, node)

            if mid + 1 < size:
                # select ix elements corresponding to iy[:mid]
                sub_ix = self.__select(iy[mid+1:], ix)
                x_var, y_var = np.var(xs[iy[mid+1:]]), np.var(ys[iy[mid+1:]])
                split_x = True if x_var > y_var else False
                # build right-subtree
                node.right = self.__build_tree(xs, ys, sub_ix, iy[mid+1:],
                                              split_x, node)

        # once it finishes recursive calls, return subtree's root node
        return node
