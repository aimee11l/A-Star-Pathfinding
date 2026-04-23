"""
Visualization Module
Creates visualizations of grids, paths, and performance metrics
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple, Dict
from .algorithms import PathfindingResult


class Visualizer:
    """Handles visualization of grids and pathfinding results"""
    
    @staticmethod
    def visualize_grid_with_path(grid: np.ndarray, path: List[Tuple[int, int]],
                                 start: Tuple[int, int], goal: Tuple[int, int],
                                 title: str = "Pathfinding Result", 
                                 filename: str = None):
        """
        Visualize grid with path, start, and goal.
        
        Args:
            grid: Grid with obstacles
            path: List of positions in path
            start: Start position
            goal: Goal position
            title: Plot title
            filename: If provided, save figure to this file
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Display grid
        grid_display = np.copy(grid).astype(float)
        grid_display[grid == 1] = 0.3  # Obstacles as gray
        
        ax.imshow(grid_display, cmap='Greys', origin='upper')
        
        # Draw path
        if len(path) > 1:
            path_array = np.array(path)
            ax.plot(path_array[:, 1], path_array[:, 0], 'b-', linewidth=2, label='Path')
        
        # Draw start and goal
        ax.plot(start[1], start[0], 'go', markersize=12, label='Start')
        ax.plot(goal[1], goal[0], 'r*', markersize=20, label='Goal')
        
        ax.set_title(title, fontsize=14)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        if filename:
            plt.savefig(filename, dpi=100, bbox_inches='tight')
            print(f"Saved visualization to {filename}")
        
        return fig, ax
    
    @staticmethod
    def visualize_search_space(grid: np.ndarray, visited_nodes: set,
                               path: List[Tuple[int, int]], 
                               start: Tuple[int, int], goal: Tuple[int, int],
                               title: str = "Search Space", 
                               filename: str = None):
        """
        Visualize grid with visited nodes and path.
        
        Args:
            grid: Grid with obstacles
            visited_nodes: Set of visited node positions
            path: Final path
            start: Start position
            goal: Goal position
            title: Plot title
            filename: If provided, save figure to this file
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Display grid
        grid_display = np.copy(grid).astype(float)
        grid_display[grid == 1] = 0.3  # Obstacles
        
        ax.imshow(grid_display, cmap='Greys', origin='upper')
        
        # Draw visited nodes
        if visited_nodes:
            visited_array = np.array(list(visited_nodes))
            ax.scatter(visited_array[:, 1], visited_array[:, 0], c='lightblue', 
                      s=10, alpha=0.5, label='Visited Nodes')
        
        # Draw path
        if len(path) > 1:
            path_array = np.array(path)
            ax.plot(path_array[:, 1], path_array[:, 0], 'b-', linewidth=2, label='Path')
        
        # Draw start and goal
        ax.plot(start[1], start[0], 'go', markersize=12, label='Start')
        ax.plot(goal[1], goal[0], 'r*', markersize=20, label='Goal')
        
        ax.set_title(title, fontsize=14)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        if filename:
            plt.savefig(filename, dpi=100, bbox_inches='tight')
            print(f"Saved visualization to {filename}")
        
        return fig, ax
    
    @staticmethod
    def compare_algorithms(results: Dict[str, PathfindingResult], 
                          metric: str = 'nodes_expanded',
                          title: str = "Algorithm Comparison",
                          filename: str = None):
        """
        Create bar chart comparing algorithms.
        
        Args:
            results: Dict mapping algorithm names to PathfindingResult objects
            metric: 'nodes_expanded', 'nodes_visited', 'path_length', or 'execution_time'
            title: Plot title
            filename: If provided, save figure to this file
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        algorithms = list(results.keys())
        values = []
        
        for algo in algorithms:
            if metric == 'nodes_expanded':
                values.append(results[algo].nodes_expanded)
            elif metric == 'nodes_visited':
                values.append(results[algo].nodes_visited)
            elif metric == 'path_length':
                values.append(results[algo].path_length)
            elif metric == 'execution_time':
                values.append(results[algo].execution_time * 1000)  # Convert to ms
        
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        bars = ax.bar(algorithms, values, color=colors[:len(algorithms)], alpha=0.7, edgecolor='black')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.1f}',
                   ha='center', va='bottom', fontsize=10)
        
        metric_labels = {
            'nodes_expanded': 'Nodes Expanded',
            'nodes_visited': 'Nodes Visited',
            'path_length': 'Path Length',
            'execution_time': 'Execution Time (ms)'
        }
        
        ax.set_ylabel(metric_labels.get(metric, metric), fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.grid(axis='y', alpha=0.3)
        
        if filename:
            plt.savefig(filename, dpi=100, bbox_inches='tight')
            print(f"Saved comparison chart to {filename}")
        
        return fig, ax
    
    @staticmethod
    def plot_performance_across_densities(density_results: Dict[float, Dict[str, PathfindingResult]],
                                         metric: str = 'nodes_expanded',
                                         title: str = "Performance vs Obstacle Density",
                                         filename: str = None):
        """
        Plot performance metrics across different obstacle densities.
        
        Args:
            density_results: Dict mapping obstacle density to algorithm results
            metric: 'nodes_expanded', 'nodes_visited', 'path_length', or 'execution_time'
            title: Plot title
            filename: If provided, save figure to this file
        """
        fig, ax = plt.subplots(figsize=(12, 7))
        
        densities = sorted(density_results.keys())
        algorithms = list(density_results[densities[0]].keys())
        
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        
        for algo_idx, algo in enumerate(algorithms):
            values = []
            for density in densities:
                result = density_results[density][algo]
                # Handle both PathfindingResult objects and aggregated stat dictionaries
                if hasattr(result, 'nodes_expanded'):
                    # It's a PathfindingResult object
                    if metric == 'nodes_expanded':
                        values.append(result.nodes_expanded)
                    elif metric == 'nodes_visited':
                        values.append(result.nodes_visited)
                    elif metric == 'path_length':
                        values.append(result.path_length)
                    elif metric == 'execution_time':
                        values.append(result.execution_time * 1000)
                else:
                    # It's a dictionary with aggregated stats
                    if metric == 'nodes_expanded':
                        values.append(result.get('avg_nodes_expanded', 0))
                    elif metric == 'nodes_visited':
                        values.append(result.get('avg_nodes_visited', 0))
                    elif metric == 'path_length':
                        values.append(result.get('avg_path_length', 0))
                    elif metric == 'execution_time':
                        values.append(result.get('avg_execution_time', 0) * 1000)
            
            ax.plot([d * 100 for d in densities], values, 
                   marker='o', linewidth=2, label=algo,
                   color=colors[algo_idx % len(colors)])
        
        metric_labels = {
            'nodes_expanded': 'Nodes Expanded',
            'nodes_visited': 'Nodes Visited',
            'path_length': 'Path Length',
            'execution_time': 'Execution Time (ms)'
        }
        
        ax.set_xlabel('Obstacle Density (%)', fontsize=12)
        ax.set_ylabel(metric_labels.get(metric, metric), fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        if filename:
            plt.savefig(filename, dpi=100, bbox_inches='tight')
            print(f"Saved performance chart to {filename}")
        
        return fig, ax
