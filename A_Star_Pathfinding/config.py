"""
Configuration file for A* pathfinding experiments
"""

# Grid Configuration
GRID_SIZE = 100  # 100x100 grid as per project requirements
MAX_GRID_SIZE = 100  # Memory limit for conventional computers

# Experiment Configuration
OBSTACLE_DENSITIES = [0.1, 0.2, 0.3]  # 10%, 20%, 30%
NUM_TRIALS_PER_CONFIG = 10  # Number of random trials per configuration
MAP_SIZES = [50, 100]  # Grid sizes to test for scalability

# Algorithm Configuration
ALLOW_DIAGONAL_MOVEMENT = False  # 4-connected grid (no diagonals)
DEFAULT_HEURISTIC = 'manhattan'  # Default heuristic function

# Heuristic Functions
HEURISTICS = {
    'manhattan': 'Manhattan distance (L1)',
    'euclidean': 'Euclidean distance (L2)',
    'zero': 'Zero heuristic (Dijkstra baseline)',
    'chebyshev': 'Chebyshev distance (L-infinity)'
}

# Output Configuration
RESULTS_DIR = 'results'
VISUALIZATIONS_DIR = 'visualizations'
REPORT_FILENAME = 'FINAL_REPORT.md'
RESULTS_JSON = 'experiment_results.json'

# Visualization Configuration
VISUALIZATION_DPI = 100
FIGURE_SIZE_SMALL = (10, 10)
FIGURE_SIZE_LARGE = (12, 7)

# Algorithm Comparison
ALGORITHMS_TO_COMPARE = [
    'A* (Manhattan)',
    'A* (Euclidean)',
    'Dijkstra',
    'BFS'
]

# Performance Thresholds (for analysis)
PERFORMANCE_THRESHOLD_NODES = {
    'EXCELLENT': 500,      # A* is excellent if < 500 nodes
    'GOOD': 1000,          # Good if < 1000 nodes
    'ACCEPTABLE': 2000,    # Acceptable if < 2000 nodes
    'POOR': 2000           # Poor if > 2000 nodes
}

# Random Seed (for reproducibility)
RANDOM_SEED_BASE = 42
RANDOM_SEED_INCREMENT = 1  # Increment seed for each trial

# Timeout Configuration
ALGORITHM_TIMEOUT_SECONDS = 30  # Maximum time to run algorithm
EXPERIMENT_TIMEOUT_SECONDS = 300  # Maximum time per experiment

# Report Generation
INCLUDE_VISUALIZATIONS_IN_REPORT = True
INCLUDE_RAW_DATA = False  # Don't include raw JSON data in report
INCLUDE_CODE_SNIPPETS = False  # Don't include code in final report

# Logging Configuration
VERBOSE = True
LOG_EVERY_N_TRIALS = 1  # Log progress every N trials
