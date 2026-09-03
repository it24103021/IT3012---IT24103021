# agent.py

from collections import deque
import heapq
import random

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

# Lab 02 - STEP 1.2 - SIMPLE REFLEX AGENT
# - Uses only the current percept
# - Uses condition-action (IF-THEN) rules
# - Has no internal memory
# - Has no percept history
# - Does not use an __init__() method
class SimpleReflexAgent:
    """Simple Reflex Agent using condition-action rules."""

    def sense_and_act(self, percept: dict) -> str:
        # IF food_here THEN Collect
        if percept["food_here"]:
            return "Collect"
        # IF wall_ahead THEN TurnLeft
        if percept["wall_ahead"]:
            return "TurnLeft"
        # ELSE Forward
        return "Forward"

# LAB 02 - STEP 1.3 - MODEL-BASED AGENT
# - Maintains an internal state
# - Records percept history
# - Records the previous action
# - Tracks estimated position
# - Tracks visited cells
# - Uses memory when selecting actions

class ModelBasedAgent:
    """Model-Based Agent that maintains an internal memory state."""

    def __init__(self):
        self.visited_cells = set() # Internal memory / state
        self.relative_position = (0, 0) # Estimated position relative to the starting position
        self.facing = "Up" # Initial direction
        self.last_action = None # Previous action
        self.percept_history = [] # Sensor/percept history
    # Helper method: Turn Left
    def turn_left(self, direction: str) -> str:
        return {
            "Up": "Left",
            "Left": "Down",
            "Down": "Right",
            "Right": "Up"
        }[direction]
    # Helper method: Turn Right
    def turn_right(self, direction: str) -> str:
        return {
            "Up": "Right",
            "Right": "Down",
            "Down": "Left",
            "Left": "Up"
        }[direction]
    # Calculate the next cell based on current position and facing direction
    def get_next_cell(self, direction: str) -> tuple:
        x, y = self.relative_position
        movement = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }
        dx, dy = movement[direction]
        return (x + dx, y + dy)

    # Agent program
    def sense_and_act(self, percept: dict) -> str:

        # SENSOR MODEL - Record the current percept.
        self.percept_history.append(dict(percept))
        # TRANSITION MODEL - Update internal state using the previous action.
        if self.last_action == "TurnLeft":
            self.facing = self.turn_left(self.facing)
        elif self.last_action == "TurnRight":
            self.facing = self.turn_right(self.facing)
        elif self.last_action == "Forward":
            # If Forward did not hit a wall,(assume that the agent moved successfully)
            if not percept.get("hit_wall", False):
                self.relative_position = self.get_next_cell(self.facing)

        # Remember current estimated position
        self.visited_cells.add(self.relative_position)

        # IF-THEN RULES USING INTERNAL MEMORY
        # IF food_here THEN Collect
        if percept["food_here"]:
            action = "Collect"
        # IF wall_ahead: IF left cell is already visited THEN TurnRight ELSE TurnLeft
        elif percept["wall_ahead"]:
            left_direction = self.turn_left(self.facing)
            left_cell = self.get_next_cell(left_direction)
            if left_cell in self.visited_cells:
                action = "TurnRight"
            else:
                action = "TurnLeft"

        # IF forward cell is already visited THEN TurnRight ELSE Forward
        else:
            forward_cell = self.get_next_cell(self.facing)
            if forward_cell in self.visited_cells:
                action = "TurnRight"
            else:
                action = "Forward"

        # Store action for the next state update
        self.last_action = action
        return action