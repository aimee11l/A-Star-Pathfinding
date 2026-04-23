"""
Experiment Runner Module
Runs comprehensive experiments comparing A*, BFS, and Dijkstra algorithms
"""

import numpy as np
import json
from typing import Dict, List, Tuple
import os
from src.grid_generator import GridGenerator
from src.algorithms import AStar, BFS, Dijkstra, PathfindingResult
from src.heuristics import Heuristic


class ExperimentRunner:
    """Runs experiments and collects statistics"""
    
    def __init__(self, grid_size: int = 100, num_trials_per_config: int = 10):
        """
        Initialize experiment runner.
        
        Args:
            grid_size: Size of grid to test
            num_trials_per_config: Number of random trials per configuration
        """
        self.grid_size = grid_size
        self.num_trials_per_config = num_trials_per_config
        self.results = {}
    
    def run_single_trial(self, grid: np.ndarray, start: Tuple[int, int], 
                        goal: Tuple[int, int]) -> Dict[str, PathfindingResult]:
        """
        Run all algorithms on a single grid configuration.
        
        Args:
            grid: Grid to search
            start: Start position
            goal: Goal position
            
        Returns:
            Dictionary of algorithm results
        """
        results = {}
        
        # A* with Manhattan heuristic
        astar = AStar()
        results['A* (Manhattan)'] = astar.search(grid, start, goal, Heuristic.manhattan)
        
        # A* with Euclidean heuristic
        results['A* (Euclidean)'] = astar.search(grid, start, goal, Heuristic.euclidean)
        
        # Dijkstra (A* with zero heuristic)
        dijkstra = Dijkstra()
        results['Dijkstra'] = dijkstra.search(grid, start, goal)
        
        # BFS
        bfs = BFS()
        results['BFS'] = bfs.search(grid, start, goal)
        
        return results
    
    def run_obstacle_density_experiment(self, obstacle_densities: List[float] = None):
        """
        Run experiments with varying obstacle densities.
        
        Args:
            obstacle_densities: List of obstacle density values to test
            
        Returns:
            Dictionary mapping density -> {algorithm -> average results}
        """
        if obstacle_densities is None:
            obstacle_densities = [0.1, 0.2, 0.3]
        
        density_results = {}
        
        for density in obstacle_densities:
            print(f"\nTesting obstacle density: {density:.1%}")
            print("-" * 60)
            
            gen = GridGenerator(self.grid_size, density)
            
            # Aggregate results across trials
            trial_results = {
                'A* (Manhattan)': [],
                'A* (Euclidean)': [],
                'Dijkstra': [],
                'BFS': []
            }
            
            successful_trials = 0
            
            for trial in range(self.num_trials_per_config):
                try:
                    # Generate random grid and positions
                    grid = gen.generate_grid(seed=None)
                    start, goal = gen.generate_start_goal(grid, seed=None)
                    
                    # Run all algorithms
                    results = self.run_single_trial(grid, start, goal)
                    
                    # Check if all algorithms found valid paths
                    all_found = all(r.success for r in results.values())
                    
                    if all_found:
                        for algo_name, result in results.items():
                            trial_results[algo_name].append({
                                'nodes_expanded': result.nodes_expanded,
                                'nodes_visited': result.nodes_visited,
                                'path_length': result.path_length,
                                'execution_time': result.execution_time
                            })
                        successful_trials += 1
                
                except Exception as e:
                    print(f"  Trial {trial}: Error - {str(e)}")
                    continue
            
            print(f"Completed {successful_trials}/{self.num_trials_per_config} successful trials")
            
            # Calculate averages
            avg_results = {}
            for algo_name, metrics_list in trial_results.items():
                if metrics_list:
                    avg_results[algo_name] = {
                        'avg_nodes_expanded': np.mean([m['nodes_expanded'] for m in metrics_list]),
                        'avg_nodes_visited': np.mean([m['nodes_visited'] for m in metrics_list]),
                        'avg_path_length': np.mean([m['path_length'] for m in metrics_list]),
                        'avg_execution_time': np.mean([m['execution_time'] for m in metrics_list]),
                        'std_nodes_expanded': np.std([m['nodes_expanded'] for m in metrics_list]),
                        'std_nodes_visited': np.std([m['nodes_visited'] for m in metrics_list]),
                        'std_path_length': np.std([m['path_length'] for m in metrics_list]),
                        'std_execution_time': np.std([m['execution_time'] for m in metrics_list]),
                        'trials': len(metrics_list)
                    }
                else:
                    avg_results[algo_name] = None
            
            density_results[density] = avg_results
            
            # Print summary
            self._print_density_summary(density, avg_results)
        
        self.results['density_experiments'] = density_results
        return density_results
    
    def run_map_size_experiment(self, map_sizes: List[int] = None, obstacle_density: float = 0.2):
        """
        Run experiments with different grid sizes.
        
        Args:
            map_sizes: List of grid sizes to test
            obstacle_density: Obstacle density for all tests
        """
        if map_sizes is None:
            map_sizes = [20, 50, 100]
        
        size_results = {}
        
        for size in map_sizes:
            print(f"\nTesting map size: {size}x{size}")
            print("-" * 60)
            
            gen = GridGenerator(size, obstacle_density)
            
            trial_results = {
                'A* (Manhattan)': [],
                'A* (Euclidean)': [],
                'Dijkstra': [],
                'BFS': []
            }
            
            successful_trials = 0
            
            for trial in range(self.num_trials_per_config):
                try:
                    grid = gen.generate_grid(seed=None)
                    start, goal = gen.generate_start_goal(grid, seed=None)
                    
                    results = self.run_single_trial(grid, start, goal)
                    
                    all_found = all(r.success for r in results.values())
                    
                    if all_found:
                        for algo_name, result in results.items():
                            trial_results[algo_name].append({
                                'nodes_expanded': result.nodes_expanded,
                                'nodes_visited': result.nodes_visited,
                                'path_length': result.path_length,
                                'execution_time': result.execution_time
                            })
                        successful_trials += 1
                
                except Exception as e:
                    print(f"  Trial {trial}: Error - {str(e)}")
                    continue
            
            print(f"Completed {successful_trials}/{self.num_trials_per_config} successful trials")
            
            # Calculate averages
            avg_results = {}
            for algo_name, metrics_list in trial_results.items():
                if metrics_list:
                    avg_results[algo_name] = {
                        'avg_nodes_expanded': np.mean([m['nodes_expanded'] for m in metrics_list]),
                        'avg_nodes_visited': np.mean([m['nodes_visited'] for m in metrics_list]),
                        'avg_path_length': np.mean([m['path_length'] for m in metrics_list]),
                        'avg_execution_time': np.mean([m['execution_time'] for m in metrics_list]),
                        'std_nodes_expanded': np.std([m['nodes_expanded'] for m in metrics_list]),
                        'std_execution_time': np.std([m['execution_time'] for m in metrics_list]),
                        'trials': len(metrics_list)
                    }
                else:
                    avg_results[algo_name] = None
            
            size_results[size] = avg_results
            self._print_size_summary(size, avg_results)
        
        self.results['size_experiments'] = size_results
        return size_results
    
    def test_edge_cases(self):
        """
        Test edge cases: unreachable goal, start == goal.
        
        Returns:
            Dictionary of edge case test results
        """
        print("\nTesting Edge Cases")
        print("=" * 60)
        
        edge_cases = {}
        gen = GridGenerator(100, 0.2)
        
        # Test 1: Start equals goal
        print("\n1. Start equals goal:")
        grid = gen.generate_grid(seed=42)
        start = goal = (50, 50)
        if grid[start[0], start[1]] == 1:
            start = goal = (49, 49)
        
        results = self.run_single_trial(grid, start, goal)
        edge_cases['start_equals_goal'] = {
            algo: {
                'success': r.success,
                'path_length': len(r.path) if r.path else 0,
                'nodes_expanded': r.nodes_expanded,
                'execution_time': r.execution_time
            }
            for algo, r in results.items()
        }
        
        for algo, result in edge_cases['start_equals_goal'].items():
            print(f"  {algo}: Success={result['success']}, Path Length={result['path_length']}")
        
        # Test 2: Goal unreachable (surrounded by obstacles)
        print("\n2. Goal surrounded by obstacles (unreachable):")
        grid = np.ones((100, 100), dtype=np.int8)
        # Create a clear start area
        grid[45:55, 45:55] = 0
        start = (50, 50)
        # Create an isolated goal
        grid[10, 10] = 0
        goal = (10, 10)
        
        results = self.run_single_trial(grid, start, goal)
        edge_cases['goal_unreachable'] = {
            algo: {
                'success': r.success,
                'nodes_expanded': r.nodes_expanded,
                'error': r.error_message
            }
            for algo, r in results.items()
        }
        
        for algo, result in edge_cases['goal_unreachable'].items():
            print(f"  {algo}: Success={result['success']}, Error={result.get('error', 'N/A')}")
        
        # Test 3: Very simple straight path
        print("\n3. Simple straight path (no obstacles):")
        grid = np.zeros((100, 100), dtype=np.int8)
        start = (50, 0)
        goal = (50, 99)
        
        results = self.run_single_trial(grid, start, goal)
        edge_cases['simple_path'] = {
            algo: {
                'success': r.success,
                'nodes_expanded': r.nodes_expanded,
                'path_length': r.path_length
            }
            for algo, r in results.items()
        }
        
        for algo, result in edge_cases['simple_path'].items():
            print(f"  {algo}: Success={result['success']}, Nodes={result['nodes_expanded']}, Length={result['path_length']:.1f}")
        
        self.results['edge_cases'] = edge_cases
        return edge_cases
    
    @staticmethod
    def _print_density_summary(density: float, results: Dict):
        """Print summary statistics for a density experiment"""
        print(f"\nResults for {density:.1%} obstacle density:")
        print("-" * 60)
        
        # Find best algorithm by nodes expanded
        best_algo = min(
            [(algo, data['avg_nodes_expanded']) for algo, data in results.items() if data],
            key=lambda x: x[1]
        )
        
        for algo, data in results.items():
            if data:
                print(f"\n{algo}:")
                print(f"  Nodes Expanded: {data['avg_nodes_expanded']:.1f} ± {data['std_nodes_expanded']:.1f}")
                print(f"  Nodes Visited:  {data['avg_nodes_visited']:.1f} ± {data['std_nodes_visited']:.1f}")
                print(f"  Path Length:    {data['avg_path_length']:.2f} ± {data['std_path_length']:.2f}")
                print(f"  Time (ms):      {data['avg_execution_time']*1000:.3f} ± {data['std_execution_time']*1000:.3f}")
        
        if best_algo:
            print(f"\nBest by nodes expanded: {best_algo[0]}")
    
    @staticmethod
    def _print_size_summary(size: int, results: Dict):
        """Print summary statistics for a size experiment"""
        print(f"\nResults for {size}x{size} grid:")
        print("-" * 60)
        
        for algo, data in results.items():
            if data:
                print(f"\n{algo}:")
                print(f"  Nodes Expanded: {data['avg_nodes_expanded']:.1f}")
                print(f"  Nodes Visited:  {data['avg_nodes_visited']:.1f}")
                print(f"  Time (ms):      {data['avg_execution_time']*1000:.3f}")
    
    def save_results(self, output_dir: str = 'results'):
        """Save experimental results to JSON file"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_to_serializable(obj):
            if isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            return obj
        
        serializable_results = convert_to_serializable(self.results)
        
        with open(os.path.join(output_dir, 'experiment_results.json'), 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"\nResults saved to {output_dir}/experiment_results.json")
    
    def print_summary_report(self):
        """Print a comprehensive summary of all experiments"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE EXPERIMENT SUMMARY")
        print("=" * 80)
        
        if 'density_experiments' in self.results:
            print("\n1. OBSTACLE DENSITY EXPERIMENTS")
            print("-" * 80)
            for density, algo_results in sorted(self.results['density_experiments'].items()):
                self._print_density_summary(density, algo_results)
        
        if 'size_experiments' in self.results:
            print("\n2. MAP SIZE EXPERIMENTS")
            print("-" * 80)
            for size, algo_results in sorted(self.results['size_experiments'].items()):
                self._print_size_summary(size, algo_results)
        
        if 'edge_cases' in self.results:
            print("\n3. EDGE CASE TESTS")
            print("-" * 80)
            print(self.results['edge_cases'])
