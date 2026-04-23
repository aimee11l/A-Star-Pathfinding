"""
Main experiment execution script
Runs all experiments and generates visualizations
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiment_runner import ExperimentRunner
from src.visualizer import Visualizer
from src.grid_generator import GridGenerator
from src.algorithms import AStar, BFS, Dijkstra
from src.heuristics import Heuristic
import numpy as np


def main():
    """Run comprehensive A* verification experiments"""
    
    print("=" * 80)
    print("A* ALGORITHM VERIFICATION AND COMPARISON EXPERIMENTS")
    print("=" * 80)
    
    # Initialize experiment runner
    runner = ExperimentRunner(grid_size=100, num_trials_per_config=5)
    
    # Run obstacle density experiments
    print("\n" + "=" * 80)
    print("PHASE 1: OBSTACLE DENSITY EXPERIMENTS")
    print("=" * 80)
    
    density_results = runner.run_obstacle_density_experiment(
        obstacle_densities=[0.1, 0.2, 0.3]
    )
    
    # Test edge cases
    print("\n" + "=" * 80)
    print("PHASE 2: EDGE CASE TESTS")
    print("=" * 80)
    
    edge_results = runner.test_edge_cases()
    
    # Run map size experiments
    print("\n" + "=" * 80)
    print("PHASE 3: MAP SIZE EXPERIMENTS")
    print("=" * 80)
    
    size_results = runner.run_map_size_experiment(
        map_sizes=[50, 100],
        obstacle_density=0.2
    )
    
    # Print comprehensive summary
    runner.print_summary_report()
    
    # Save results
    runner.save_results('results')
    
    # Generate visualizations
    print("\n" + "=" * 80)
    print("PHASE 4: GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    gen = GridGenerator(100, 0.2)
    grid = gen.generate_grid(seed=42)
    start, goal = gen.generate_start_goal(grid, seed=42)
    
    # Run algorithms for visualization
    astar = AStar()
    dijkstra = Dijkstra()
    bfs = BFS()
    
    astar_result = astar.search(grid, start, goal, Heuristic.manhattan)
    dijkstra_result = dijkstra.search(grid, start, goal)
    bfs_result = bfs.search(grid, start, goal)
    
    os.makedirs('visualizations', exist_ok=True)
    
    # Visualize individual results
    if astar_result.success:
        Visualizer.visualize_grid_with_path(
            grid, astar_result.path, start, goal,
            title=f"A* Algorithm Result (Nodes: {astar_result.nodes_expanded})",
            filename='visualizations/astar_path.png'
        )
    
    if dijkstra_result.success:
        Visualizer.visualize_grid_with_path(
            grid, dijkstra_result.path, start, goal,
            title=f"Dijkstra Algorithm Result (Nodes: {dijkstra_result.nodes_expanded})",
            filename='visualizations/dijkstra_path.png'
        )
    
    if bfs_result.success:
        Visualizer.visualize_grid_with_path(
            grid, bfs_result.path, start, goal,
            title=f"BFS Algorithm Result (Nodes: {bfs_result.nodes_expanded})",
            filename='visualizations/bfs_path.png'
        )
    
    # Comparison chart
    results = {
        'A* (Manhattan)': astar_result,
        'Dijkstra': dijkstra_result,
        'BFS': bfs_result
    }
    
    Visualizer.compare_algorithms(
        results,
        metric='nodes_expanded',
        title='Algorithm Comparison: Nodes Expanded',
        filename='visualizations/comparison_nodes_expanded.png'
    )
    
    Visualizer.compare_algorithms(
        results,
        metric='execution_time',
        title='Algorithm Comparison: Execution Time',
        filename='visualizations/comparison_execution_time.png'
    )
    
    # Performance across densities
    if density_results:
        Visualizer.plot_performance_across_densities(
            density_results,
            metric='nodes_expanded',
            title='Performance vs Obstacle Density: Nodes Expanded',
            filename='visualizations/density_nodes_expanded.png'
        )
        
        Visualizer.plot_performance_across_densities(
            density_results,
            metric='execution_time',
            title='Performance vs Obstacle Density: Execution Time',
            filename='visualizations/density_execution_time.png'
        )
    
    print("\nAll visualizations saved to 'visualizations/' directory")
    print("\n" + "=" * 80)
    print("EXPERIMENT COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()
