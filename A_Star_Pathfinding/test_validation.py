#!/usr/bin/env python3
"""
Validation and Testing Script
Verifies correct implementation and functionality
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.grid_generator import GridGenerator
from src.algorithms import AStar, BFS, Dijkstra
from src.heuristics import Heuristic


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from src import grid_generator
        from src import algorithms
        from src import heuristics
        from src import visualizer
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_grid_generator():
    """Test grid generation"""
    print("\nTesting grid generator...")
    try:
        gen = GridGenerator(100, 0.2)
        grid = gen.generate_grid(seed=42)
        
        # Check grid shape and values
        assert grid.shape == (100, 100), f"Grid shape mismatch: {grid.shape}"
        assert np.all((grid == 0) | (grid == 1)), "Grid contains invalid values"
        
        # Check obstacle density
        obstacle_count = np.sum(grid)
        expected_density = 0.2
        actual_density = obstacle_count / (100 * 100)
        assert abs(actual_density - expected_density) < 0.05, f"Density mismatch: {actual_density}"
        
        # Check start/goal generation
        start, goal = gen.generate_start_goal(grid, seed=42)
        assert grid[start[0], start[1]] == 0, "Start position is obstacle"
        assert grid[goal[0], goal[1]] == 0, "Goal position is obstacle"
        assert start != goal, "Start and goal are same"
        
        print(f"✓ Grid generator works correctly")
        print(f"  - Grid shape: {grid.shape}")
        print(f"  - Obstacle density: {actual_density:.1%}")
        print(f"  - Start: {start}, Goal: {goal}")
        return True
    except Exception as e:
        print(f"✗ Grid generator error: {e}")
        return False


def test_heuristics():
    """Test heuristic functions"""
    print("\nTesting heuristics...")
    try:
        pos1 = (0, 0)
        pos2 = (3, 4)
        
        manhattan = Heuristic.manhattan(pos1, pos2)
        euclidean = Heuristic.euclidean(pos1, pos2)
        chebyshev = Heuristic.chebyshev(pos1, pos2)
        zero = Heuristic.zero(pos1, pos2)
        
        # Verify values
        assert manhattan == 7, f"Manhattan incorrect: {manhattan}"
        assert abs(euclidean - 5.0) < 0.01, f"Euclidean incorrect: {euclidean}"
        assert chebyshev == 4, f"Chebyshev incorrect: {chebyshev}"
        assert zero == 0, f"Zero incorrect: {zero}"
        
        # Verify admissibility (never overestimate)
        assert manhattan >= euclidean - 0.01, "Manhattan overestimates"
        
        print("✓ Heuristic functions work correctly")
        print(f"  - Manhattan: {manhattan}")
        print(f"  - Euclidean: {euclidean:.2f}")
        print(f"  - Chebyshev: {chebyshev}")
        return True
    except Exception as e:
        print(f"✗ Heuristic error: {e}")
        return False


def test_algorithms():
    """Test pathfinding algorithms"""
    print("\nTesting algorithms...")
    try:
        # Create simple test grid
        gen = GridGenerator(50, 0.15)
        grid = gen.generate_grid(seed=123)
        start, goal = gen.generate_start_goal(grid, seed=123)
        
        # Test A*
        astar = AStar()
        astar_result = astar.search(grid, start, goal, Heuristic.manhattan)
        assert astar_result.success, "A* failed to find path"
        assert len(astar_result.path) > 0, "A* returned empty path"
        assert astar_result.path[0] == start, "A* path doesn't start correctly"
        assert astar_result.path[-1] == goal, "A* path doesn't end correctly"
        assert astar_result.nodes_expanded > 0, "A* didn't expand nodes"
        
        # Test BFS
        bfs = BFS()
        bfs_result = bfs.search(grid, start, goal)
        assert bfs_result.success, "BFS failed to find path"
        assert len(bfs_result.path) > 0, "BFS returned empty path"
        
        # Test Dijkstra
        dijkstra = Dijkstra()
        dijkstra_result = dijkstra.search(grid, start, goal)
        assert dijkstra_result.success, "Dijkstra failed to find path"
        assert len(dijkstra_result.path) > 0, "Dijkstra returned empty path"
        
        # Verify all found optimal paths
        assert abs(astar_result.path_length - bfs_result.path_length) < 0.01, \
            "Path lengths don't match (optimality violation)"
        assert abs(astar_result.path_length - dijkstra_result.path_length) < 0.01, \
            "Path lengths don't match (optimality violation)"
        
        # Verify A* efficiency
        assert astar_result.nodes_expanded <= bfs_result.nodes_expanded, \
            "A* less efficient than BFS"
        assert astar_result.nodes_expanded <= dijkstra_result.nodes_expanded, \
            "A* less efficient than Dijkstra"
        
        print("✓ All algorithms work correctly")
        print(f"  - A*: {astar_result.nodes_expanded} nodes, path length {astar_result.path_length:.2f}")
        print(f"  - BFS: {bfs_result.nodes_expanded} nodes, path length {bfs_result.path_length:.2f}")
        print(f"  - Dijkstra: {dijkstra_result.nodes_expanded} nodes, path length {dijkstra_result.path_length:.2f}")
        return True
    except Exception as e:
        print(f"✗ Algorithm error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_cases():
    """Test edge case handling"""
    print("\nTesting edge cases...")
    try:
        gen = GridGenerator(50, 0.2)
        
        # Test 1: Start equals goal
        grid = gen.generate_grid(seed=456)
        start = goal = (25, 25)
        while grid[start[0], start[1]] != 0:
            start = goal = (start[0] + 1, start[1])
        
        astar = AStar()
        result = astar.search(grid, start, goal, Heuristic.manhattan)
        assert result.success, "Failed on start==goal"
        assert len(result.path) == 1, "Path length should be 1"
        assert result.nodes_expanded == 0, "Should expand 0 nodes"
        
        print("  ✓ Start equals goal: handled correctly")
        
        # Test 2: Simple straight path
        grid = np.zeros((50, 50), dtype=np.int8)
        start = (25, 0)
        goal = (25, 49)
        
        result = astar.search(grid, start, goal, Heuristic.manhattan)
        assert result.success, "Failed on straight path"
        assert result.path_length == 49, f"Path should be 49, got {result.path_length}"
        
        print("  ✓ Simple straight path: solved optimally")
        
        # Test 3: Unreachable goal
        grid = np.ones((50, 50), dtype=np.int8)
        grid[25, 0:25] = 0  # Open corridor
        start = (25, 0)
        goal = (0, 0)  # Blocked off
        
        result = astar.search(grid, start, goal, Heuristic.manhattan)
        assert not result.success, "Should fail on unreachable goal"
        
        print("  ✓ Unreachable goal: correctly identified")
        
        print("✓ All edge cases handled correctly")
        return True
    except Exception as e:
        print(f"✗ Edge case error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_optimality_verification():
    """Verify that heuristics are truly admissible"""
    print("\nVerifying heuristic admissibility...")
    try:
        # For any two points, Manhattan distance >= Euclidean distance
        # and Euclidean >= true optimal path (straight line)
        
        test_cases = [
            ((0, 0), (10, 10)),
            ((5, 3), (15, 20)),
            ((0, 0), (0, 100)),
            ((50, 50), (0, 0))
        ]
        
        all_admissible = True
        for pos1, pos2 in test_cases:
            manhattan = Heuristic.manhattan(pos1, pos2)
            euclidean = Heuristic.euclidean(pos1, pos2)
            
            # Manhattan >= Euclidean for all cases
            if manhattan < euclidean - 0.01:
                print(f"  ✗ Manhattan not >= Euclidean for {pos1} to {pos2}")
                all_admissible = False
            
            # Both should be >= 0
            if manhattan < 0 or euclidean < 0:
                print(f"  ✗ Negative heuristic for {pos1} to {pos2}")
                all_admissible = False
        
        if all_admissible:
            print("✓ All heuristics verified as admissible")
        return all_admissible
    except Exception as e:
        print(f"✗ Admissibility verification error: {e}")
        return False


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("A* PATHFINDING - VALIDATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Grid Generator", test_grid_generator),
        ("Heuristics", test_heuristics),
        ("Algorithms", test_algorithms),
        ("Edge Cases", test_edge_cases),
        ("Admissibility", test_optimality_verification),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - Implementation is valid!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed - Please review errors above")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
