"""
Grid World Generator Module
Generates parameterized grid maps with configurable obstacle density
"""

import numpy as np
from typing import Tuple


class GridGenerator:
    """
    Generates random grid maps with obstacles.
    
    Attributes:
        grid_size: Size of the grid (grid_size x grid_size)
        obstacle_density: Proportion of obstacles (0.0 to 1.0)
    """
    
    def __init__(self, grid_size: int = 100, obstacle_density: float = 0.2):
        """
        Initialize grid generator.
        
        Args:
            grid_size: Dimension of square grid (100 for this project)
            obstacle_density: Fraction of cells that are obstacles
        """
        if not (0 <= obstacle_density <= 1.0):
            raise ValueError("obstacle_density must be between 0 and 1")
        if grid_size <= 0:
            raise ValueError("grid_size must be positive")
            
        self.grid_size = grid_size
        self.obstacle_density = obstacle_density
    
    def generate_grid(self, seed: int = None) -> np.ndarray:
        """
        Generate a random grid with obstacles.
        
        Args:
            seed: Random seed for reproducibility
            
        Returns:
            2D numpy array where 0 = free space, 1 = obstacle
        """
        if seed is not None:
            np.random.seed(seed)
        
        grid = np.random.choice(
            [0, 1],
            size=(self.grid_size, self.grid_size),
            p=[1 - self.obstacle_density, self.obstacle_density]
        )
        
        return grid.astype(np.int8)
    
    def generate_start_goal(self, grid: np.ndarray, seed: int = None) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Generate random start and goal positions that are not obstacles.
        
        Args:
            grid: The grid to place start and goal on
            seed: Random seed for reproducibility
            
        Returns:
            Tuple of (start_position, goal_position) where positions are (row, col)
        """
        if seed is not None:
            np.random.seed(seed)
        
        free_cells = np.argwhere(grid == 0)
        
        if len(free_cells) < 2:
            raise ValueError("Grid has fewer than 2 free cells for start and goal")
        
        indices = np.random.choice(len(free_cells), size=2, replace=False)
        start = tuple(free_cells[indices[0]])
        goal = tuple(free_cells[indices[1]])
        
        return start, goal
    
    @staticmethod
    def is_valid_position(grid: np.ndarray, position: Tuple[int, int]) -> bool:
        """
        Check if a position is valid (within bounds and not an obstacle).
        
        Args:
            grid: The grid
            position: (row, col) position
            
        Returns:
            True if position is valid
        """
        row, col = position
        return (0 <= row < grid.shape[0] and 
                0 <= col < grid.shape[1] and 
                grid[row, col] == 0)
