import random
import math

def path_cost(problem, path):
    """Calculates the total cost of a path."""
    cost = 0
    for i in range(len(path) - 1):
        cost += problem.get_cost(path[i+1], i+1)
    return cost

def get_neighbors(problem, path):
    """Generates neighbors of a path by making a small modification."""
    neighbors = []
    if len(path) > 2:
        # Simple neighbor: slightly perturb one point in the path
        idx_to_change = random.randint(1, len(path) - 2)
        original_node = path[idx_to_change]
        
        # Get a valid action from the previous node in the path
        prev_node = path[idx_to_change - 1]
        
        actions = problem.get_actions(prev_node)
        if actions:
            new_action = random.choice(actions)
            new_node = problem.get_result(prev_node, new_action)
            
            # Ensure the new node is not an obstacle and is within bounds
            if new_node not in problem.static_obstacles:
                new_path = list(path)
                new_path[idx_to_change] = new_node
                # From here, we would need to replan the rest of the path,
                # which is complex. For this example, we'll keep it simple
                # and just return this slightly modified path.
                neighbors.append(new_path)
    return neighbors


def hill_climbing_random_restarts(problem, initial_path, max_restarts=10):
    """Hill-climbing with random restarts for path replanning."""
    best_path = initial_path
    best_cost = path_cost(problem, best_path)

    for _ in range(max_restarts):
        current_path = list(best_path) # Start from the best path found so far
        
        while True:
            neighbors = get_neighbors(problem, current_path)
            if not neighbors:
                break # No better neighbors

            # Find the best neighbor
            next_path = min(neighbors, key=lambda p: path_cost(problem, p))
            next_cost = path_cost(problem, next_path)

            if next_cost >= path_cost(problem, current_path):
                break # Reached a local minimum
            
            current_path = next_path
        
        current_cost = path_cost(problem, current_path)
        if current_cost < best_cost:
            best_path = current_path
            best_cost = current_cost
            
    return best_path, best_cost
