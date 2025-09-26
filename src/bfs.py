from collections import deque
from src.grid_city import Node

def bfs(problem):
    """Breadth-First Search algorithm."""
    start_node = Node(problem.start)
    if problem.is_goal(start_node.state):
        return [], 0, 1 # path, cost, nodes expanded

    frontier = deque([start_node])
    explored = {problem.start}
    nodes_expanded = 0

    while frontier:
        nodes_expanded += 1
        node = frontier.popleft()

        for action in problem.get_actions(node.state):
            child_state = problem.get_result(node.state, action)
            if child_state not in explored:
                child_node = Node(child_state, node, action, node.path_cost + 1)
                if problem.is_goal(child_node.state):
                    return _reconstruct_path(child_node), child_node.path_cost, nodes_expanded
                frontier.append(child_node)
                explored.add(child_state)
    return None, float('inf'), nodes_expanded

def _reconstruct_path(node):
    """Helper to reconstruct the path from a goal node."""
    path = []
    while node.parent:
        path.append(node.state)
        node = node.parent
    path.append(node.state)
    return path[::-1]
