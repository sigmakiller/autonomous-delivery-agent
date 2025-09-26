import heapq
from src.grid_city import Node

def ucs(problem):
    """Uniform-Cost Search algorithm."""
    start_node = Node(problem.start, path_cost=0)
    frontier = [(start_node.path_cost, start_node)]
    explored = set()
    nodes_expanded = 0

    while frontier:
        nodes_expanded += 1
        cost, node = heapq.heappop(frontier)

        if node.state in explored:
            continue
        explored.add(node.state)

        if problem.is_goal(node.state):
            return _reconstruct_path(node), node.path_cost, nodes_expanded

        for action in problem.get_actions(node.state):
            child_state = problem.get_result(node.state, action)
            step_cost = problem.get_cost(child_state)
            new_cost = node.path_cost + step_cost
            child_node = Node(child_state, node, action, new_cost)
            heapq.heappush(frontier, (child_node.path_cost, child_node))

    return None, float('inf'), nodes_expanded

def _reconstruct_path(node):
    """Helper to reconstruct the path from a goal node."""
    path = []
    while node.parent:
        path.append(node.state)
        node = node.parent
    path.append(node.state)
    return path[::-1]
