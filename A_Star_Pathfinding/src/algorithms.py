"""
Pathfinding Algorithms Module
Implements A*, BFS, and Dijkstra's algorithm
"""

import numpy as np
from typing import Tuple, List, Callable, Dict, Optional
from queue import PriorityQueue
from collections import deque
import time


class PathfindingResult:
    """Data class to store pathfinding results"""
    
    def __init__(self):
        self.path: List[Tuple[int, int]] = []
        self.nodes_expanded: int = 0
        self.nodes_visited: int = 0
        self.execution_time: float = 0.0
        self.path_length: float = 0.0
        self.success: bool = False
        self.error_message: str = ""


class Pathfinder:
    """Base class for pathfinding algorithms"""
    
    # Directions: up, down, left, right, and 4 diagonals
    DIRECTIONS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    DIRECTIONS_8 = [(-1, 0), (1, 0), (0, -1), (0, 1),
                    (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    @staticmethod
    def get_neighbors(position: Tuple[int, int], grid: np.ndarray, 
                      allow_diagonal: bool = False) -> List[Tuple[int, int]]:
        """
        Get valid neighbors for a position.
        
        Args:
            position: Current position (row, col)
            grid: The grid
            allow_diagonal: Whether to allow diagonal movement
            
        Returns:
            List of valid neighbor positions
        """
        directions = Pathfinder.DIRECTIONS_8 if allow_diagonal else Pathfinder.DIRECTIONS_4
        neighbors = []
        
        for dr, dc in directions:
            new_row = position[0] + dr
            new_col = position[1] + dc
            
            if (0 <= new_row < grid.shape[0] and 
                0 <= new_col < grid.shape[1] and 
                grid[new_row, new_col] == 0):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    @staticmethod
    def get_distance(pos1: Tuple[int, int], pos2: Tuple[int, int], 
                     allow_diagonal: bool = False) -> float:
        """
        Calculate movement cost between two adjacent positions.
        
        Args:
            pos1: First position
            pos2: Second position
            allow_diagonal: Whether diagonal movement is allowed
            
        Returns:
            Movement cost (1 for orthogonal, sqrt(2) for diagonal)
        """
        if allow_diagonal and pos1[0] != pos2[0] and pos1[1] != pos2[1]:
            return np.sqrt(2)  # Diagonal move
        return 1.0  # Orthogonal move


class AStar(Pathfinder):
    """A* Pathfinding Algorithm"""
    
    def search(self, grid: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int],
               heuristic: Callable = None, allow_diagonal: bool = False) -> PathfindingResult:
        """
        Perform A* search.
        
        Args:
            grid: Grid with obstacles (0 = free, 1 = obstacle)
            start: Start position (row, col)
            goal: Goal position (row, col)
            heuristic: Heuristic function h(current, goal)
            allow_diagonal: Whether to allow diagonal movement
            
        Returns:
            PathfindingResult with path and statistics
        """
        result = PathfindingResult()
        start_time = time.time()
        
        try:
            # Input validation
            if not self._validate_inputs(grid, start, goal, result):
                result.execution_time = time.time() - start_time
                return result
            
            if heuristic is None:
                from .heuristics import Heuristic
                heuristic = Heuristic.manhattan
            
            # Initialize
            open_list = PriorityQueue()
            closed_set = set()
            
            g_score = {start: 0}
            f_score = {start: heuristic(start, goal)}
            
            open_list.put((f_score[start], id(start), start))
            parent = {start: None}
            
            nodes_expanded = 0
            
            while not open_list.empty():
                _, _, current = open_list.get()
                
                if current == goal:
                    result.path = self._reconstruct_path(parent, current)
                    result.path_length = self._calculate_path_length(result.path, allow_diagonal)
                    result.nodes_expanded = nodes_expanded
                    result.nodes_visited = len(closed_set)
                    result.success = True
                    result.execution_time = time.time() - start_time
                    return result
                
                if current in closed_set:
                    continue
                
                closed_set.add(current)
                nodes_expanded += 1
                
                for neighbor in self.get_neighbors(current, grid, allow_diagonal):
                    if neighbor in closed_set:
                        continue
                    
                    movement_cost = self.get_distance(current, neighbor, allow_diagonal)
                    tentative_g = g_score[current] + movement_cost
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        parent[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                        open_list.put((f_score[neighbor], id(neighbor), neighbor))
            
            # No path found
            result.error_message = "No path found (goal unreachable)"
            result.nodes_expanded = nodes_expanded
            result.nodes_visited = len(closed_set)
            
        except Exception as e:
            result.error_message = str(e)
        
        result.execution_time = time.time() - start_time
        return result
    
    @staticmethod
    def _validate_inputs(grid: np.ndarray, start: Tuple[int, int], 
                        goal: Tuple[int, int], result: PathfindingResult) -> bool:
        """Validate algorithm inputs"""
        if start == goal:
            result.path = [start]
            result.nodes_expanded = 0
            result.nodes_visited = 0
            result.path_length = 0.0
            result.success = True
            return False
        
        if grid[start[0], start[1]] != 0:
            result.error_message = "Start position is an obstacle"
            return False
        
        if grid[goal[0], goal[1]] != 0:
            result.error_message = "Goal position is an obstacle"
            return False
        
        return True
    
    @staticmethod
    def _reconstruct_path(parent: Dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Reconstruct path from parent pointers"""
        path = [current]
        while parent[current] is not None:
            current = parent[current]
            path.append(current)
        path.reverse()
        return path
    
    @staticmethod
    def _calculate_path_length(path: List[Tuple[int, int]], allow_diagonal: bool) -> float:
        """Calculate total path length"""
        if len(path) <= 1:
            return 0.0
        
        total = 0.0
        for i in range(len(path) - 1):
            total += Pathfinder.get_distance(path[i], path[i+1], allow_diagonal)
        return total


class BFS(Pathfinder):
    """Breadth-First Search Algorithm"""
    
    def search(self, grid: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int],
               allow_diagonal: bool = False) -> PathfindingResult:
        """
        Perform BFS search.
        
        Args:
            grid: Grid with obstacles (0 = free, 1 = obstacle)
            start: Start position (row, col)
            goal: Goal position (row, col)
            allow_diagonal: Whether to allow diagonal movement
            
        Returns:
            PathfindingResult with path and statistics
        """
        result = PathfindingResult()
        start_time = time.time()
        
        try:
            if start == goal:
                result.path = [start]
                result.nodes_expanded = 0
                result.nodes_visited = 0
                result.path_length = 0.0
                result.success = True
                result.execution_time = time.time() - start_time
                return result
            
            if grid[start[0], start[1]] != 0 or grid[goal[0], goal[1]] != 0:
                result.error_message = "Start or goal is an obstacle"
                result.execution_time = time.time() - start_time
                return result
            
            queue = deque([start])
            visited = {start}
            parent = {start: None}
            nodes_expanded = 0
            
            while queue:
                current = queue.popleft()
                nodes_expanded += 1
                
                if current == goal:
                    result.path = AStar._reconstruct_path(parent, current)
                    result.path_length = AStar._calculate_path_length(result.path, allow_diagonal)
                    result.nodes_expanded = nodes_expanded
                    result.nodes_visited = len(visited)
                    result.success = True
                    result.execution_time = time.time() - start_time
                    return result
                
                for neighbor in self.get_neighbors(current, grid, allow_diagonal):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        parent[neighbor] = current
                        queue.append(neighbor)
            
            result.error_message = "No path found (goal unreachable)"
            result.nodes_expanded = nodes_expanded
            result.nodes_visited = len(visited)
            
        except Exception as e:
            result.error_message = str(e)
        
        result.execution_time = time.time() - start_time
        return result


class Dijkstra(Pathfinder):
    """Dijkstra's Algorithm (equivalent to A* with zero heuristic)"""
    
    def search(self, grid: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int],
               allow_diagonal: bool = False) -> PathfindingResult:
        """
        Perform Dijkstra's search.
        
        Args:
            grid: Grid with obstacles (0 = free, 1 = obstacle)
            start: Start position (row, col)
            goal: Goal position (row, col)
            allow_diagonal: Whether to allow diagonal movement
            
        Returns:
            PathfindingResult with path and statistics
        """
        result = PathfindingResult()
        start_time = time.time()
        
        try:
            if start == goal:
                result.path = [start]
                result.nodes_expanded = 0
                result.nodes_visited = 0
                result.path_length = 0.0
                result.success = True
                result.execution_time = time.time() - start_time
                return result
            
            if grid[start[0], start[1]] != 0 or grid[goal[0], goal[1]] != 0:
                result.error_message = "Start or goal is an obstacle"
                result.execution_time = time.time() - start_time
                return result
            
            open_list = PriorityQueue()
            closed_set = set()
            
            g_score = {start: 0}
            open_list.put((0, id(start), start))
            parent = {start: None}
            
            nodes_expanded = 0
            
            while not open_list.empty():
                _, _, current = open_list.get()
                
                if current == goal:
                    result.path = AStar._reconstruct_path(parent, current)
                    result.path_length = AStar._calculate_path_length(result.path, allow_diagonal)
                    result.nodes_expanded = nodes_expanded
                    result.nodes_visited = len(closed_set)
                    result.success = True
                    result.execution_time = time.time() - start_time
                    return result
                
                if current in closed_set:
                    continue
                
                closed_set.add(current)
                nodes_expanded += 1
                
                for neighbor in self.get_neighbors(current, grid, allow_diagonal):
                    if neighbor in closed_set:
                        continue
                    
                    movement_cost = self.get_distance(current, neighbor, allow_diagonal)
                    tentative_g = g_score[current] + movement_cost
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        parent[neighbor] = current
                        g_score[neighbor] = tentative_g
                        open_list.put((tentative_g, id(neighbor), neighbor))
            
            result.error_message = "No path found (goal unreachable)"
            result.nodes_expanded = nodes_expanded
            result.nodes_visited = len(closed_set)
            
        except Exception as e:
            result.error_message = str(e)
        
        result.execution_time = time.time() - start_time
        return result
