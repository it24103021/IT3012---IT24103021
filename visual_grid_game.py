# visual_grid_game.py
import random
import tkinter as tk

from agent import SearchAgent

class VisualGridHuntGame:
    # Lab 01,Lab 01 """A flexible Pacman-style grid environment with support for configurable opponents and larger scales."""
    """ The SearchAgent receives a global model containing:Agent position, Grid size, Walls, Food positions
    This allows the agent to perform offline search."""

    def __init__(self, width=10, height=10, num_food=10, custom_walls=None):
                 # Lab 01, Lab 02 num_opponents=2, num_traps=5
        
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]  # Starting position (x, y)

        # Lab 02 - Step 1.1: Store the direction the agent is currently facing.
        # This is required to calculate "wall_ahead".
        # self.agent_facing = "Up"

        if custom_walls is not None:
            self.walls = set(
                tuple(wall)
                for wall in custom_walls
            )
        else:
            # Generate some default scattered walls for a larger grid
            self.walls = {(2, 2), (2, 3), (5, 5), (6, 5), (3, 7)}

        # Dynamically generate random food positions avoiding walls and agent start
        self.food_positions = set()
        while len(self.food_positions) < num_food:
            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)
            pos_tuple = (fx, fy)
            if pos_tuple != (0, 0) and pos_tuple not in self.walls:
                self.food_positions.add(pos_tuple)


        # Lab 01 - Step 2.1.1 - Q9: Initialize toxic traps
        # self.toxic_traps = set()
        # while len(self.toxic_traps) < num_traps:
        #    tx = random.randint(0, self.width - 1)
        #    ty = random.randint(0, self.height - 1)
        #    trap_pos = (tx, ty)
        #    if (
        #        trap_pos != (0, 0)
        #        and trap_pos not in self.walls
        #        and trap_pos not in self.food_positions
        #    ):
        #        self.toxic_traps.add(trap_pos)

        # Generate adversarial opponents    
        # self.opponents = []
        # while len(self.opponents) < num_opponents:
        #    ox = random.randint(0, self.width - 1)
        #    oy = random.randint(0, self.height - 1)
        #    op_pos = [ox, oy]
        #    if (
        #        tuple(op_pos) != (0, 0) 
        #        and tuple(op_pos) not in self.walls 
        #        and tuple(op_pos) not in self.food_positions 
        #        # Lab 01 - Step 2.1.1 - Q9: Prevent opponents from spawning on toxic traps
        #        and tuple(op_pos) not in self.toxic_traps
        #    ):
        #        self.opponents.append(op_pos)

        self.score = 0
        self.steps = 0
        self.collision = False
        self.hit_wall = False

    def get_percept(self) -> dict:

        # Lab 02 - Step 1.1 - PARTIAL OBSERVABILITY
        # Do NOT return exact agent_pos or all opponent positions.Only return local sensor information.
        # x, y = self.agent_pos
        # direction_vectors = {"Up": (0, 1),
        #                     "Down": (0, -1),
        #                     "Left": (-1, 0),
        #                     "Right": (1, 0)}
        # dx, dy = direction_vectors[self.agent_facing]
        # ahead_x = x + dx
        # ahead_y = y + dy

        # Check whether the cell ahead is outside the grid
        # outside_grid = (ahead_x < 0 
        #                or ahead_x >= self.width
        #                or ahead_y < 0 
        #                or ahead_y >= self.height)

        # Lab 02 - Step 1.1 - Local boolean sensor
        # wall_ahead = (outside_grid or (ahead_x, ahead_y) in self.walls)

        return {
            # Lab 02 - Step 1.1 - Only local percepts are returned.
            #"wall_ahead": wall_ahead,
            "food_here": tuple(self.agent_pos) in self.food_positions,
            #"opponent_here": any(op == self.agent_pos for op in self.opponents), # Local information only
            #"toxin_here": tuple(self.agent_pos) in self.toxic_traps,
            'hit_wall': self.hit_wall,
            'collision': self.collision,

            # Lab 01
            'agent_pos': list(self.agent_pos),
            #'opponent_positions': [list(op) for op in self.opponents],
            #'smells_food': tuple(self.agent_pos) in self.food_positions,
            # Lab 01 - Step 2.2.1 - Q10: Add toxin sensor to the agent's percept
            #'smells_toxin': tuple(self.agent_pos) in self.toxic_traps,
            'score': self.score,
            'remaining_food': len(self.food_positions),

            # Lab 03 - GLOBAL PERCEPT
            "grid_size": (self.width, self.height),
            "walls": list(self.walls),
            "all_food": list(self.food_positions),
        }

    def execute_action(self, action: str):
        self.steps += 1
        self.hit_wall = False

        # Lab 02 - Supporting modification
        # Lab 01 used:Up, Down, Left, Right || Lab 02 uses:Forward, TurnLeft, TurnRight, Collect
        # left_turn = {"Up": "Left", 
        #             "Left": "Down",
        #             "Down": "Right", 
        #             "Right": "Up"}
        # right_turn = {"Up": "Right", 
        #              "Right": "Down",
        #              "Down": "Left", 
        #              "Left": "Up"}

        # Lab 02 - Turning action
        # if action == "TurnLeft":
        #    self.agent_facing = left_turn[self.agent_facing]
        # elif action == "TurnRight":
        #    self.agent_facing = right_turn[self.agent_facing]

        # Lab 02 - Step 1.2 - IF food_here THEN Collect
        # elif action == "Collect":
        #    current_pos = tuple(self.agent_pos)
        #    if current_pos in self.food_positions:
        #        self.food_positions.remove(current_pos)
        #        self.score += 20

        # Lab 02 - Steps 1.2 and 1.3 - Move one cell in the current facing direction.
        # elif action == "Forward":
        #    movement = {"Up": (0, 1), 
        #                "Down": (0, -1),
        #                "Left": (-1, 0), 
        #                "Right": (1, 0) }
        #    dx, dy = movement[self.agent_facing]

        # Lab 03 - MOVEMENT ACTIONS
        if action in (
            "Up",
            "Down",
            "Left",
            "Right"
        ):
            movement = {
                "Up": (0, 1),
                "Down": (0, -1),
                "Left": (-1, 0),
                "Right": (1, 0)
            }
            dx, dy = movement[action]

            new_pos = [self.agent_pos[0] + dx,
                       self.agent_pos[1] + dy]
            outside_grid = (new_pos[0] < 0 
                            or new_pos[0] >= self.width
                            or new_pos[1] < 0 
                            or new_pos[1] >= self.height)

            if outside_grid or tuple(new_pos) in self.walls:
                self.score -= 5
                self.hit_wall = True

            else:
                self.agent_pos = new_pos
                # Lab 01 - Step 2.3 - Q11 Toxic trap penalty retained from Lab 01.
                # if tuple(self.agent_pos) in self.toxic_traps:
                #    self.score -= 15

        # COLLECT FOOD
        elif action == "Collect":
            current_position = tuple(self.agent_pos)
            if current_position in self.food_positions:
                self.food_positions.remove(current_position)
                self.score += 20

        # Lab 01      
        #new_pos = list(self.agent_pos)
        #if action == 'Up':
        #    new_pos[1] = min(self.height - 1, new_pos[1] + 1)
        #elif action == 'Down':
        #    new_pos[1] = max(0, new_pos[1] - 1)
        #elif action == 'Left':
        #    new_pos[0] = max(0, new_pos[0] - 1)
        #elif action == 'Right':
        #    new_pos[0] = min(self.width - 1, new_pos[0] + 1)
        #moved = False
        #if tuple(new_pos) in self.walls:
        #    self.score -= 5 
        #    self.hit_wall = True
        #else:
        #    self.agent_pos = new_pos 
        #    moved = True

        #tuple_pos = tuple(self.agent_pos)

        #if tuple_pos in self.food_positions:
        #    self.food_positions.remove(tuple_pos)
        #    self.score += 20


        # Lab 01 - Step 2.3.1 / Q11: Apply a 15-point penalty when the agent enters a toxic trap
        #if moved and tuple_pos in self.toxic_traps:
        #    self.score -= 15

        # for op in self.opponents:
        #    move = random.choice(['Up', 'Down', 'Left', 'Right', 'Stay'])
        #    new_op = list(op)
        #    if move == 'Up' and new_op[1] < self.height - 1:
        #        new_op[1] += 1
        #    elif move == 'Down' and new_op[1] > 0:
        #        new_op[1] -= 1
        #    elif move == 'Left' and new_op[0] > 0:
        #        new_op[0] -= 1
        #    elif move == 'Right' and new_op[0] < self.width - 1:
        #        new_op[0] += 1

        #    if tuple(new_op) not in self.walls:
        #        op[0] = new_op[0]
        #        op[1] = new_op[1]

        #    if op == self.agent_pos:
        #        self.score -= 50
        #        self.collision = True
    
    # GAME TERMINATION
    def is_done(self):
        # Game finishes when:
        # 1. All food is collected OR Maximum steps are reached
        return (
            len(self.food_positions) == 0 or self.steps >= 100 or self.collision )

# LAB 02 - STEP 1.2 - SIMPLE REFLEX AGENT
# Important: No __init__() method, No memory, No percept history, Uses only current percept + IF-THEN rules.
# class SimpleReflexAgent:
#    """A simple reflex agent that acts purely on current percepts using IF-THEN rules."""

#    def sense_and_act(self, percept: dict) -> str:
         # Lab 02 - Step 1.2, CONDITION-ACTION RULE 1, IF food_here THEN Collect
#        if percept["food_here"]:
#            return "Collect"
         # Lab 02 - Step 1.2, CONDITION-ACTION RULE 2, IF wall_ahead THEN TurnLeft
#        if percept["wall_ahead"]:
#            return "TurnLeft"
         # Lab 02 - Step 1.2, CONDITION-ACTION RULE 3, ELSE Forward
#        return "Forward"

# LAB 02 - STEP 1.3 - MODEL-BASED AGENT
# Maintains an internal memory/state.
# class ModelBasedAgent:
#    """A model-based agent that uses memory of visited cells."""

#    def __init__(self):

        # Lab 02 - Step 1.3 - Internal memory of visited locations.
#        self.visited_cells = set()
#        self.relative_position = (0, 0)
#        self.facing = "Up"
#        self.last_action = None
#        self.percept_history = []

#    def turn_left(self, direction: str) -> str:
#        return {"Up": "Left",
#                "Left": "Down",
#                "Down": "Right",
#                "Right": "Up"}[direction]

#    def turn_right(self, direction: str) -> str:
#        return {"Up": "Right",
#                "Right": "Down",
#                "Down": "Left",
#                "Left": "Up"}[direction]

#    def get_next_cell(self, direction: str) -> tuple:
#        x, y = self.relative_position
#        movement = {"Up": (0, 1),
#                    "Down": (0, -1),
#                    "Left": (-1, 0),
#                    "Right": (1, 0)}
#        dx, dy = movement[direction]
#        return (x + dx, y + dy)

#    def sense_and_act(self, percept: dict) -> str:
#
         # Lab 02 - Step 1.3 - SENSOR MODEL, Record the current percept.
#        self.percept_history.append(dict(percept))

         # Lab 02 - Step 1.3 - TRANSITION MODEL, Update internal state using the previous action.
#        if self.last_action == "TurnLeft":
#            self.facing = self.turn_left(self.facing)
#        elif self.last_action == "TurnRight":
#            self.facing = self.turn_right(self.facing)
#        elif self.last_action == "Forward":
             # If the previous Forward action did not hit a wall,the agent assumes that it moved successfully.
#            if not percept.get("hit_wall", False):
#                self.relative_position = (self.get_next_cell(self.facing))

         # Lab 02 - Step 1.3 - Remember current estimated position.
#        self.visited_cells.add(self.relative_position)

         # Lab 02 - Step 1.3 - IF-THEN RULES USING MEMORY
         # IF food_here THEN Collect
#        if percept["food_here"]:
#            action = "Collect"
         # IF wall_ahead AND left_is_visited: THEN TurnRight
#        elif percept["wall_ahead"]:
#            left_direction = self.turn_left(self.facing)
#            left_cell = self.get_next_cell(left_direction)
#            action = "TurnRight" if left_cell in self.visited_cells else "TurnLeft"  # We already explored left.
#        else:
#            forward_cell = self.get_next_cell(self.facing)
             # Lab 02 - Step 1.3 - Detect a repeated path using memory.
#            action = "TurnRight" if forward_cell in self.visited_cells else "Forward" # Try another direction instead of repeating the same route.

         # Lab 02 - Step 1.3 - Store the action for the next state update.
#        self.last_action = action
#        return action

class GridGameGUI:
    """Tkinter wrapper that dynamically scales cell sizes to keep larger grids on screen."""

    def __init__(self, root, width=10, height=10, num_food=12, walls=None, algorithm="BFS"):
        # Lab 01, Lab 02 num_opponents=2, num_traps=5, agent_type="simple"
        self.root = root
        self.root.title("IT3012 - Search Agent")

        self.env = VisualGridHuntGame(
            width=width, height=height, num_food=num_food, 
            # num_traps=num_traps, num_opponents=num_opponents,
            custom_walls=walls)

        # CREATE SEARCH AGENT
        self.agent = SearchAgent(algorithm=algorithm)
        self.agent_name = (f"Search Agent - {algorithm}")

        # Lab 02 - Steps 1.2 and 1.3 - Select which agent architecture to run.
        # if agent_type == "model":
        #    self.agent = ModelBasedAgent()
        #    self.agent_name = "Model-Based Agent"
        # else:
        #    self.agent = SimpleReflexAgent()
        #    self.agent_name = "Simple Reflex Agent"
        
        # Dynamically calculate cell size so the total canvas fits nicely within a 600x600 window ceiling
        max_canvas_dim = 600
        self.cell_size = max(20, min(max_canvas_dim // self.env.width, 
                                     max_canvas_dim // self.env.height))

        canvas_w = self.env.width * self.cell_size
        canvas_h = self.env.height * self.cell_size

        self.canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg="white")
        self.canvas.pack()

        self.label = tk.Label(root, text=(f"{self.agent_name} | " "Score: 0 | Steps: 0") , font=("Arial", 14))
        self.label.pack(pady=10)

        self.btn = tk.Button(root, text="Start Simulation", command=self.run_loop,  
                             font=("Arial", 12),bg="#000066",fg="white")
        self.btn.pack(pady=5)
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")

        for x in range(self.env.width):
            for y in range(self.env.height):
                x1 = x * self.cell_size
                y1 = (self.env.height - 1 - y) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Lab 01,02 --> color = "#f1f5f9" if (x, y) not in self.env.walls else "#64748b"
                if (x, y) in self.env.walls: self.canvas.create_rectangle(x1, y1, x2, y2, fill="#64748b", outline="#cbd5e1")
                else:self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f1f5f9", outline="#cbd5e1")

                # Only draw text if cell is large enough
                # if self.cell_size >= 40 and (x, y) in self.env.walls:
                #    self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text="W", fill="white",
                #                            font=("Arial", 8, "bold"))


        # Lab 01 - Step 2.3.2 - Q11: Render toxic traps as purple shapes
        # for tx, ty in self.env.toxic_traps:
        #    offset = self.cell_size * 0.25
        #    x1 = tx * self.cell_size + offset
        #    y1 = (self.env.height - 1 - ty) * self.cell_size + offset
        #    self.canvas.create_rectangle(
        #        x1, y1, x1 + self.cell_size * 0.5, y1 + self.cell_size * 0.5,
        #            fill="#9333ea", outline="#6b21a8"
        #    )

        for fx, fy in self.env.food_positions:
            offset = self.cell_size * 0.25
            x1 = fx * self.cell_size + offset
            y1 = (self.env.height - 1 - fy) * self.cell_size + offset
            self.canvas.create_oval(x1, y1, x1 + self.cell_size * 0.5, y1 + self.cell_size * 0.5, 
                    fill="#f59e0b", outline="#d97706")

        # for ox, oy in self.env.opponents:
        #    offset = self.cell_size * 0.2
        #    x1 = ox * self.cell_size + offset
        #    y1 = (self.env.height - 1 - oy) * self.cell_size + offset
        #    self.canvas.create_rectangle(x1, y1, x1 + self.cell_size * 0.6, y1 + self.cell_size * 0.6, 
        #            fill="#990000", outline="#7a0000")

        ax, ay = self.env.agent_pos
        offset = self.cell_size * 0.15
        x1 = ax * self.cell_size + offset
        y1 = (self.env.height - 1 - ay) * self.cell_size + offset
        self.canvas.create_oval(x1, y1, x1 + self.cell_size * 0.7, y1 + self.cell_size * 0.7, 
                    fill="#000066", outline="#1e3a8a")

    def run_loop(self):
        """Run the game simulation."""

        self.btn.config(state="disabled")

        def step():
            if not self.env.is_done():
                # Lab 02 - SENSOR Environment -> get_percept()
                percept = self.env.get_percept()
                # Lab 02 - AGENT PROGRAM,Percept -> sense_and_act()
                action = self.agent.sense_and_act(percept)
                # Lab 02 - ACTUATOR,Execute selected action.
                self.env.execute_action(action)

                self.draw_grid()
                self.label.config(text=f"{self.agent_name} | Score: {self.env.score} | Steps: {self.env.steps} | Action: {action}")
                self.root.after(250, step)
            else:
                # if self.env.collision:
                #    end_text = f"Collision! Game Over! Final Score: {self.env.score}"

                if len(self.env.food_positions) == 0:
                    end_text = (
                        "All Food Collected! | " f"Final Score: {self.env.score} | " f"Steps: {self.env.steps}")
                elif self.env.steps >= 100:
                    end_text = (
                        "Maximum Steps Reached | " f"Final Score: {self.env.score}")
                else:
                    end_text = f"Finished! Final Score: {self.env.score}" 
                self.label.config(text=end_text)
                self.btn.config(state="normal")

        step()

if __name__ == "__main__":
    root = tk.Tk()
    # Lab 01,02 Try a larger grid size like 12x12 with 15 food and 3 opponents!

    # LAB 03 - SELECT SEARCH ALGORITHM --> Use one of: "BFS", "DFS", "UCS"
    SEARCH_ALGORITHM = "BFS"
    app = GridGameGUI(root, width=12, height=12, num_food=15, algorithm=SEARCH_ALGORITHM)
    # Lab 02 num_opponents=3, num_traps=5, agent_type="simple"
    # Step 1.3 - Change agent_type= "simple" --> "model"
    root.mainloop()