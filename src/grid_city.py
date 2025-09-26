import heapq

class Node:
    """A node class for search algorithms."""
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, other):
        return self.path_cost < other.path_cost

class GridCity:
    """Represents the 2D grid city environment."""
    def __init__(self, map_file):
        self.static_obstacles = set()
        self.terrain_costs = {}
        self.dynamic_obstacles = {}
        self.start = None
        self.goal = None
        self.width = 0
        self.height = 0
        self._load_map(map_file)

    def _load_map(self, map_file):
        """Loads the map from a file."""
        with open(map_file, 'r') as f:
            for r, row in enumerate(f):
                self.height = r + 1
                self.width = len(row.strip())
                for c, char in enumerate(row.strip()):
                    pos = (r, c)
                    if char == '#':
                        self.static_obstacles.add(pos)
                    elif char.isdigit():
                        self.terrain_costs[pos] = int(char)
                    elif char == 'S':
                        self.start = pos
                        self.terrain_costs[pos] = 1
                    elif char == 'G':
                        self.goal = pos
                        self.terrain_costs[pos] = 1
                    elif char == 'D': # Dynamic obstacle
                        # Format: D:t1,r1,c1;t2,r2,c2
                        parts = row.strip().split(':')
                        if len(parts) > 1:
                            schedule_str = parts[1]
                            schedule = {}
                            for item in schedule_str.split(';'):
                                t, r_dyn, c_dyn = map(int, item.split(','))
                                schedule[t] = (r_dyn, c_dyn)
                            self.dynamic_obstacles[pos] = schedule
                        self.terrain_costs[pos] = 1 # Default cost
                    else:
                        self.terrain_costs[pos] = 1 # Default cost

    def get_actions(self, state):
        """Returns valid actions from a given state."""
        r, c = state
        actions = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-connected
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width and (nr, nc) not in self.static_obstacles:
                actions.append((dr, dc))
        return actions

    def get_result(self, state, action):
        """Returns the new state after taking an action."""
        r, c = state
        dr, dc = action
        return (r + dr, c + dc)

    def get_cost(self, state, time_step=0):
        """Gets the cost of a cell, considering dynamic obstacles."""
        if state in self.terrain_costs:
            cost = self.terrain_costs[state]
            for schedule in self.dynamic_obstacles.values():
                if time_step in schedule and schedule[time_step] == state:
                    return float('inf') # Collision with dynamic obstacle
            return cost
        return 1

    def is_goal(self, state):
        """Checks if a state is the goal."""
        return state == self.goal
