"""
Heuristic Functions Module
Implements admissible heuristic functions for A* algorithm
"""

import numpy as np
from typing import Tuple


class Heuristic:
    """Base class for heuristic functions"""
    
    @staticmethod
    def manhattan(current: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """
        Manhattan distance heuristic (L1 distance).
        Admissible for grid-based movement with 4-connectivity.
        
        Args:
            current: Current position (row, col)
            goal: Goal position (row, col)
            
        Returns:
            Manhattan distance
        """
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
    
    @staticmethod
    def euclidean(current: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """
        Euclidean distance heuristic (L2 distance).
        Admissible for grid-based movement with 8-connectivity.
        
        Args:
            current: Current position (row, col)
            goal: Goal position (row, col)
            
        Returns:
            Euclidean distance
        """
        dy = abs(current[0] - goal[0])
        dx = abs(current[1] - goal[1])
        return np.sqrt(dx**2 + dy**2)
      
    @staticmethod
    def zero(current: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """
        Zero heuristic (degenerates to Dijkstra's algorithm).
        Used for comparison purposes.
        
        Args:
            current: Current position (row, col)
            goal: Goal position (row, col)
            
        Returns:
            Always 0
        """
        return 0.0
    
    @staticmethod
    def chebyshev(current: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """
        Chebyshev distance (maximum of absolute differences).
        Admissible for 8-connected grid movement (diagonal allowed).
        
        Args:
            current: Current position (row, col)
            goal: Goal position (row, col)
            
        Returns:
            Chebyshev distance
        """
        return max(abs(current[0] - goal[0]), abs(current[1] - goal[1]))
  
