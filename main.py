import argparse
import time
from src.grid_city import GridCity
from src.bfs import bfs
from src.ucs import ucs
from src.a_star import a_star
from src.local_search import hill_climbing_random_restarts

def main():
    parser = argparse.ArgumentParser(description="Run delivery agent planners.")
    parser.add_argument("map", help="Path to the map file.")
    parser.add_argument("planner", choices=['bfs', 'ucs', 'a_star', 'replan'], help="Planner to use.")
    args = parser.parse_args()

    city = GridCity(args.map)
    
    print(f"Running {args.planner.upper()} on {args.map}")
    print(f"Start: {city.start}, Goal: {city.goal}")

    start_time = time.time()
    
    if args.planner == 'bfs':
        path, cost, expanded = bfs(city)
    elif args.planner == 'ucs':
        path, cost, expanded = ucs(city)
    elif args.planner == 'a_star':
        path, cost, expanded = a_star(city)
    elif args.planner == 'replan':
        print("\n--- Initial A* Plan ---")
        initial_path, initial_cost, initial_expanded = a_star(city)
        if initial_path:
            print(f"Initial Path Found: Cost={initial_cost}, Length={len(initial_path)}")
            print(f"Nodes Expanded: {initial_expanded}")
            
            # --- Simulate a dynamic obstacle appearing ---
            new_obstacle_pos = initial_path[len(initial_path) // 2]
            city.static_obstacles.add(new_obstacle_pos)
            print(f"\n!!! Dynamic Obstacle appeared at {new_obstacle_pos} !!!")
            print("--- Replanning with Hill-Climbing ---")

            # A* to get a new baseline path for local search
            new_initial_path, _, _ = a_star(city) 
            
            if new_initial_path:
                path, cost = hill_climbing_random_restarts(city, new_initial_path)
                expanded = "N/A for local search"
            else:
                 path, cost, expanded = None, float('inf'), 0
        else:
            path, cost, expanded = None, float('inf'), 0
            
    end_time = time.time()

    print("\n--- Results ---")
    if path:
        print(f"Path: {path}")
        print(f"Path Cost: {cost}")
        print(f"Nodes Expanded: {expanded}")
    else:
        print("No path found.")
        
    print(f"Time taken: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()
