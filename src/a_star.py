import heapq
from src.grid_city import Node

def manhattan_distance(state, goal):
    """Admissible heuristic: Manhattan distance."""
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

def a_star(problem, heuristic=manhattan_distance):
    """A* search algorithm."""
    start_node = Node(problem.start, path_cost=0)
    frontier = [(0, start_node)]
    explored = set()
    nodes_expanded = 0

    while frontier:
        nodes_expanded += 1
        _, node = heapq.heappop(frontier)

        if node.state in explored:
            continue
        explored.add(node.state)

        if problem.is_goal(node.state):
            return _reconstruct_path(node), node.path_cost, nodes_expanded

        for action in problem.get_actions(node.state):
            child_state = problem.get_result(node.state, action)
            step_cost = problem.get_cost(child_state, node.depth + 1)
            new_cost = node.path_cost + step_cost
            child_node = Node(child_state, node, action, new_cost)

            priority = new_cost + heuristic(child_state, problem.goal)
            heapq.heappush(frontier, (priority, child_node))

    return None, float('inf'), nodes_expanded

def _reconstruct_path(node):
    """Helper to reconstruct the path from a goal node."""
    path = []
    while node.parent:
        path.append(node.state)
        node = node.parent
    path.append(node.state)
    return path[::-1]
