# Autonomous Delivery Agent Pathfinding

This project is an implementation of an autonomous delivery agent designed to navigate a 2D grid-based city. The agent's goal is to find the most efficient path from a starting point to a destination, intelligently handling static obstacles, varied terrain costs, and dynamic, moving obstacles.

This work was completed for the "CSA2001-Fundamentals of AI and ML" course. It features the implementation and experimental comparison of several fundamental AI search algorithms.

## Features

  - **2D Grid City Environment:** The agent operates in a grid world loaded from custom map files. The environment includes:
      - Start (`S`) and Goal (`G`) points.
      - Static Obstacles (`#`): Impassable walls.
      - Variable Terrain Costs (`1-9`): Cells with different integer movement costs.
      - Dynamic Obstacles (`D`): Obstacles that appear at specific locations at given times according to a known schedule.
  - **Multiple Pathfinding Algorithms:** A suite of classic AI search algorithms to find and compare paths.
  - **Dynamic Replanning:** A local search mechanism to adapt the agent's path when unexpected obstacles appear.
  - **Performance Analysis:** The program outputs the found path, total cost, nodes expanded, and execution time for performance comparison.

## Algorithms Implemented

This project provides an implementation and comparison of the following search strategies:

#### 1\. Uninformed Search

These algorithms search the state space without any prior knowledge about the cost or distance to the goal.

  - **Breadth-First Search (BFS):** Explores the grid layer by layer. It guarantees finding the shortest path in terms of the number of steps but does not consider terrain costs.
  - **Uniform-Cost Search (UCS):** An extension of Dijkstra's algorithm. It explores the grid by always expanding the node with the lowest path cost from the start. It guarantees finding the path with the minimum total cost.

#### 2\. Informed Search

This algorithm uses a heuristic function to guide the search toward the goal more efficiently.

  - **A\* Search:** Combines the strengths of UCS with a heuristic. It prioritizes nodes that have both a low path cost and are estimated to be close to the goal. We use the **Manhattan Distance** as an admissible heuristic, which ensures A\* will find the optimal (lowest-cost) path.

#### 3\. Local Search for Replanning

This strategy is used for adapting an existing plan when the environment changes unexpectedly.

  - **Hill-Climbing with Random Restarts:** When a pre-calculated path is blocked by a new obstacle, this algorithm makes small, incremental changes to the path to navigate around it. It's a fast but non-optimal approach ideal for quick replanning.

## Getting Started

### Prerequisites

  - Python 3.x

No external libraries are required to run this project.

### Installation & Execution

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd <repository-name>
    ```

3.  **Run a planner:**
    Use the `main.py` script, which provides a command-line interface (CLI), to run the planners.

    **Syntax:**

    ```bash
    python main.py <path_to_map_file> <planner_name>
    ```

      - `<path_to_map_file>`: The relative path to the map file (e.g., `medium.txt`).
      - `<planner_name>`: The algorithm to use. Choices are: `bfs`, `ucs`, `a_star`, `replan`.

-----

## Usage Examples

#### 1\. Breadth-First Search (BFS)

Finds the path with the fewest steps.

```bash
python main.py medium.txt bfs
```

#### 2\. Uniform-Cost Search (UCS)

Finds the path with the lowest total travel cost.

```bash
python main.py medium.txt ucs
```

#### 3\. A\* Search

Efficiently finds the lowest-cost path using the Manhattan distance heuristic.

```bash
python main.py medium.txt a_star
```

#### 4\. Dynamic Replanning (A\* with Hill-Climbing)

Simulates a scenario where an A\* path is blocked and the agent must replan using local search. This demonstrates the required proof-of-concept for dynamic replanning.

```bash
python main.py dynamic.txt replan
```

-----

## Map File Format

The grid city is defined by `.txt` files. The characters represent different elements:

  - `S`: Starting position of the agent.
  - `G`: Goal/delivery location.
  - `.`: Standard terrain with a movement cost of 1.
  - `#`: A static, impassable obstacle (wall).
  - `1`-`9`: Terrain with a higher movement cost, equal to the number's value.
  - `D`: A cell associated with a dynamic obstacle schedule.

**Dynamic Obstacle Schedule:**
To define when and where dynamic obstacles appear, add a line at the end of the map file with the following format:

`D:<r1>,<c1>,<t1>;<r2>,<c2>,<t2>;...`

  - `<r>`: Row of the obstacle.
  - `<c>`: Column of the obstacle.
  - `<t>`: Time step at which the obstacle is at that `(r, c)` position.

**Example Map (`dynamic.txt`):**

```
S...
.D..
...G
D:1,1,2;2,1,3;3,2,3
```

## Algorithm Analysis

A key goal of this project is to analyze when each search method performs better.

  - **BFS** is optimal for finding the shortest path in terms of steps. It performs best on maps where all terrain costs are uniform (cost of 1), as its exhaustive layer-by-layer search is very efficient. However, it performs poorly when path cost is the primary metric on varied-terrain maps.

  - **UCS** is the best choice when the goal is to find the guaranteed lowest-cost path on a map with variable terrain costs. It expands nodes strictly in order of their cost from the source. Its major drawback is that it explores in all directions, often expanding many nodes that are not in the direction of the goal.

  - **A\*** is generally the most effective algorithm. By using an admissible heuristic (Manhattan distance), it directs its search toward the goal, significantly reducing the number of expanded nodes compared to UCS while still guaranteeing an optimal solution. It almost always outperforms UCS in both time and nodes expanded.

  - **Hill-Climbing Replanner** is not a complete search algorithm but a reactive strategy. Its strength lies in its speed for making minor adjustments to an existing path when the environment changes. It is not guaranteed to find an optimal new path, but it is excellent for dynamic situations where a quick, "good enough" solution is needed immediately.
