import math
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
