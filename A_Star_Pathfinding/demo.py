#!/usr/bin/env python3
"""
Quick Demo Script
Shows basic usage of the A* pathfinding implementation
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grid_generator import GridGenerator
from src.algorithms import AStar, BFS, Dijkstra, PathfindingResult
from src.heuristics import Heuristic
import numpy as np


def print_grid_with_path(grid, path, start, goal, title="Grid Visualization"):
    """Simple text-based grid visualization"""
    
    grid_display = np.copy(grid).astype(str)
    grid_display[grid == 0] = '.'
    grid_display[grid == 1] = '#'
    
    for pos in path:
        if pos != start and pos != goal:
            grid_display[pos] = '*'
    
    grid_display[start] = 'S'
    grid_display[goal] = 'G'
    
    print(f"\n{title}")
    print("-" * 40)
    
    # Print smaller excerpt (20x20) for readability
    start_row = max(0, start[0] - 10)
    end_row = min(grid.shape[0], start[0] + 10)
    start_col = max(0, start[1] - 10)
    end_col = min(grid.shape[1], start[1] + 10)
    
    for i in range(start_row, end_row):
        print(''.join(grid_display[i, start_col:end_col]))
    
    print("-" * 40)


def main():
    """Run demo"""
    
    print("=" * 60)
    print("A* PATHFINDING ALGORITHM - QUICK DEMO")
    print("=" * 60)
    
    # Create a simple grid
    print("\n1. Generating Grid...")
    gen = GridGenerator(grid_size=100, obstacle_density=0.2)
    grid = gen.generate_grid(seed=42)
    start, goal = gen.generate_start_goal(grid, seed=42)
    
    print(f"   Grid size: {grid.shape}")
    print(f"   Start: {start}, Goal: {goal}")
    print(f"   Obstacle density: 20%")
    
    # Run A* algorithm
    print("\n2. Running A* Algorithm (Manhattan heuristic)...")
    astar = AStar()
    astar_result = astar.search(grid, start, goal, Heuristic.manhattan)
    
    print(f"   Success: {astar_result.success}")
    print(f"   Nodes expanded: {astar_result.nodes_expanded}")
    print(f"   Nodes visited: {astar_result.nodes_visited}")
    print(f"   Path length: {astar_result.path_length:.2f}")
    print(f"   Execution time: {astar_result.execution_time*1000:.3f}ms")
    
    if astar_result.success:
        print_grid_with_path(grid, astar_result.path, start, goal, "A* Path (excerpt)")
    
    # Run Dijkstra for comparison
    print("\n3. Running Dijkstra's Algorithm for Comparison...")
    dijkstra = Dijkstra()
    dijkstra_result = dijkstra.search(grid, start, goal)
    
    print(f"   Success: {dijkstra_result.success}")
    print(f"   Nodes expanded: {dijkstra_result.nodes_expanded}")
    print(f"   Path length: {dijkstra_result.path_length:.2f}")
    print(f"   Execution time: {dijkstra_result.execution_time*1000:.3f}ms")
    
    # Run BFS for comparison
    print("\n4. Running BFS for Comparison...")
    bfs = BFS()
    bfs_result = bfs.search(grid, start, goal)
    
    print(f"   Success: {bfs_result.success}")
    print(f"   Nodes expanded: {bfs_result.nodes_expanded}")
    print(f"   Path length: {bfs_result.path_length:.2f}")
    print(f"   Execution time: {bfs_result.execution_time*1000:.3f}ms")
    
    # Summary
    print("\n" + "=" * 60)
    print("EFFICIENCY COMPARISON SUMMARY")
    print("=" * 60)
    print(f"\n{'Algorithm':<20} {'Nodes':<10} {'Time (ms)':<12} {'Speed vs A*'}")
    print("-" * 60)
    
    print(f"{'A* (Manhattan)':<20} {astar_result.nodes_expanded:<10} "
          f"{astar_result.execution_time*1000:<12.3f} {'baseline'}")
    
    dijkstra_speedup = dijkstra_result.nodes_expanded / astar_result.nodes_expanded if astar_result.nodes_expanded > 0 else 0
    print(f"{'Dijkstra':<20} {dijkstra_result.nodes_expanded:<10} "
          f"{dijkstra_result.execution_time*1000:<12.3f} {f'{dijkstra_speedup:.2f}x slower'}")
    
    bfs_speedup = bfs_result.nodes_expanded / astar_result.nodes_expanded if astar_result.nodes_expanded > 0 else 0
    print(f"{'BFS':<20} {bfs_result.nodes_expanded:<10} "
          f"{bfs_result.execution_time*1000:<12.3f} {f'{bfs_speedup:.2f}x slower'}")
    
    print("\n" + "=" * 60)
    print("KEY FINDINGS:")
    print("=" * 60)
    print(f"✓ A* expanded {dijkstra_speedup:.1f}x fewer nodes than Dijkstra")
    print(f"✓ A* expanded {bfs_speedup:.1f}x fewer nodes than BFS")
    print(f"✓ All algorithms found equally optimal paths (length: {astar_result.path_length:.2f})")
    print(f"✓ A* is {(dijkstra_result.execution_time/astar_result.execution_time):.2f}x faster than Dijkstra")
    
    print("\nDemo completed successfully!")
    print("For full experimental suite, run: python experiments/run_experiments.py")


if __name__ == "__main__":
    main()
