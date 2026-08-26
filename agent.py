# agent.py
from collections import deque
import heapq
# import random

# Lab 01,Lab 02 - OLD AGENT
# class GreedyGridAgent:
#    """A simple agent that tries to move around systematically to clear the grid."""
#    def __init__(self):
#        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
#    def sense_and_act(self, percept: dict) -> str:
#        # If standing directly on food, or just wander / move towards coordinates
#        pos = percept['agent_pos']
#        # Simple heuristic or fallback random sweep
#        return random.choice(self.actions_pool)

# Lab 02 - SIMPLE REFLEX AGENT
# class SimpleReflexAgent:
#     def sense_and_act(self, percept):
#         if percept["food_here"]:
#             return "Collect"
#         if percept["wall_ahead"]:
#             return "TurnLeft"
#         return "Forward"

# LAB 02 - MODEL-BASED AGENT
# class ModelBasedAgent:
#     def __init__(self):
#         self.visited_cells = set()
#         self.relative_position = (0, 0)
#         self.facing = "Up"
#         self.last_action = None
#         self.percept_history = []
#     def turn_left(self, direction):
#         return {
#             "Up": "Left",
#             "Left": "Down",
#             "Down": "Right",
#             "Right": "Up"}[direction]
#     def turn_right(self, direction):
#         return {
#             "Up": "Right",
#             "Right": "Down",
#             "Down": "Left",
#             "Left": "Up"}[direction]
#     def get_next_cell(self, direction):
#         x, y = self.relative_position
#         movement = {
#             "Up": (0, 1),
#             "Down": (0, -1),
#             "Left": (-1, 0),
#             "Right": (1, 0)}
#         dx, dy = movement[direction]
#         return (x + dx, y + dy)
#
#     def sense_and_act(self, percept):
#         self.percept_history.append(dict(percept))
#         if self.last_action == "TurnLeft":
#             self.facing = self.turn_left(self.facing)
#         elif self.last_action == "TurnRight":
#             self.facing = self.turn_right(self.facing)
#         elif self.last_action == "Forward":
#             if not percept.get("hit_wall", False):
#                 self.relative_position = self.get_next_cell(self.facing)
#         self.visited_cells.add(self.relative_position)
#         if percept["food_here"]:action = "Collect"
#         elif percept["wall_ahead"]:
#             left_direction = self.turn_left(self.facing)
#             left_cell = self.get_next_cell(left_direction)
#             action = "TurnRight" if left_cell in self.visited_cells else "TurnLeft"
#         else:
#             forward_cell = self.get_next_cell(self.facing)
#             action = "TurnRight" if forward_cell in self.visited_cells else "Forward"
#         self.last_action = action
#         return action


# Lab 03 - SEARCH AGENT
# The SearchAgent uses:
#     1. Breadth-First Search (BFS)
#     2. Depth-First Search (DFS)
#     3. Uniform-Cost Search (UCS)
# The agent receives:
#     - Current agent position
#     - Grid size
#     - Wall positions
#     - Food positions
# The agent then:
#     1. Selects a food target.
#     2. Searches for a path.
#     3. Stores the path as a plan.
#     4. Executes one action at a time.

# Lab 03 - Step 1.2.1 - SEARCH AGENT
class SearchAgent:

    # Lab 03 - Step 1.2.3 - Select search algorithms: BFS, DFS, or UCS
    def __init__(self, algorithm="BFS"):
        self.active_algo = algorithm.upper()
        self.plan = []

    # Generate valid neighboring states for search
    def get_neighbors(self, position, walls, grid_size):
        """Return all valid neighboring states.
        Each result has the form:(new_position, action)"""

        x, y = position
        width, height = grid_size
        moves = [
            ((0, 1), "Up"),
            ((1, 0), "Right"),
            ((0, -1), "Down"),
            ((-1, 0), "Left")]
        neighbors = []

        for (dx, dy), action in moves:
            new_x = x + dx
            new_y = y + dy
            new_position = (new_x, new_y)
            inside_grid = (0 <= new_x < width and 0 <= new_y < height)
            not_wall = new_position not in walls
            if inside_grid and not_wall:
                neighbors.append((new_position, action))
        return neighbors

    # LaB 03 - Step 1.2.3 - BREADTH-FIRST SEARCH
    def bfs_search(self, start, goal, walls, grid_size):
        """BFS uses a FIFO queue.
        Because every movement has the same cost,BFS finds a shortest path in terms of 
        number of movements."""

        start = tuple(start)
        goal = tuple(goal)
        walls = {
            tuple(wall)
            for wall in walls
        }

        # FIFO queue.
        queue = deque()
        queue.append((start, []))
        reached = {start}
        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path
            for neighbor, action in self.get_neighbors(
                current,
                walls,
                grid_size
            ):
                if neighbor not in reached:
                    reached.add(neighbor)
                    new_path = path + [action]
                    queue.append((neighbor, new_path))
        return None

    # Lab 03 -Step 1.2.4 - DEPTH-FIRST SEARCH
    def dfs_search(self, start, goal, walls, grid_size):
        """DFS uses a LIFO stack.
        DFS does not guarantee the shortest path."""

        start = tuple(start)
        goal = tuple(goal)
        walls = {
            tuple(wall)
            for wall in walls
        }

        # LIFO stack.
        stack = []
        stack.append((start, []))
        reached = {start}
        while stack:
            current, path = stack.pop()
            if current == goal:
                return path
            for neighbor, action in self.get_neighbors(
                current,
                walls,
                grid_size
            ):
                if neighbor not in reached:
                    reached.add(neighbor)
                    new_path = path + [action]
                    stack.append((neighbor, new_path))
        return None

    # Lab 03 - Step 1.2.5 - UNIFORM-COST SEARCH
    def ucs_search(self, start, goal, walls, grid_size):
        """UCS expands the state with the lowest path cost.
        In this environment: Every movement = cost 1
        Therefore, UCS normally finds the same shortest path length as BFS.
        """

        start = tuple(start)
        goal = tuple(goal)
        walls = {
            tuple(wall)
            for wall in walls
        }

        frontier = []
        counter = 0
        heapq.heappush(
            frontier,
            (0, counter, start, [])
        )
        reached = {start: 0}
        while frontier:
            cost, _, current, path = heapq.heappop(frontier)
            if current == goal:
                return path
            for neighbor, action in self.get_neighbors(
                current,
                walls,
                grid_size
            ):
                new_cost = cost + 1
                if (neighbor not in reached
                    or new_cost < reached[neighbor]):
                    reached[neighbor] = new_cost
                    counter += 1
                    new_path = path + [action]
                    heapq.heappush(
                        frontier,
                            (new_cost,
                            counter,
                            neighbor,
                            new_path)
                    )
        return None

    # Lab 03 - SEARCH DISPATCHER
    def search(self, start, goal, walls, grid_size):
        """Select and execute the requested search algorithm."""
        if self.active_algo == "BFS":
            return self.bfs_search(
                start,
                goal,
                walls,
                grid_size
            )
        elif self.active_algo == "DFS":
            return self.dfs_search(
                start,
                goal,
                walls,
                grid_size
            )
        elif self.active_algo == "UCS":
            return self.ucs_search(
                start,
                goal,
                walls,
                grid_size
            )
        else:
            raise ValueError(f"Unknown search algorithm: {self.active_algo}")

    # Lab 03 - SENSE AND ACT
    def sense_and_act(self, percept):
        """Agent program.
        The agent:
            1. Checks whether food is at the current position.
            2. If yes, collects it.
            3. If there is no plan, creates a search plan.
            4. Executes one action from the plan."""

        # Collect food if the agent is already standing on a food position.
        if percept["food_here"]:
            self.plan = []
            return "Collect"
        
        # If there is no existing plan, create a new plan.
        if not self.plan:
            start = tuple(percept["agent_pos"])
            grid_size = percept["grid_size"]
            walls = { tuple(wall) for wall in percept["walls"] }
            all_food = { tuple(food) for food in percept["all_food"] }
            if not all_food:
                return "Collect"
            # Select the closest food using Manhattan distance.
            goal = min(
                all_food,
                key=lambda food:
                    abs(start[0] - food[0]) + abs(start[1] - food[1])
            )
            self.plan = self.search(
                start,
                goal,
                walls,
                grid_size
            )
            if self.plan is None:
                self.plan = []
            # Display search information in terminal.
            print("Algorithm :", self.active_algo)
            print("Start     :", start)
            print("Goal      :", goal)
            print("Plan      :", self.plan)
            print("Path Cost :", len(self.plan))

        # Execute the next planned action.
        if self.plan:
            return self.plan.pop(0)

        # No path available.
        return "Collect"