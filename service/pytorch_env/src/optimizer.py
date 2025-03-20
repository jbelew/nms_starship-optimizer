import random
import math
import copy
import json

from itertools import permutations
from modules_refactored import modules

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [
            [
                {
                    "module": None,
                    "label": None,
                    "value": 0,
                    "type": "",
                    "total": 0.0,
                    "adjacency_bonus": 0.0,
                    "bonus": 0.0,
                    "active": True,
                    "adjacency": False,
                    "tech": None,
                    "supercharged": False,
                    "sc_eligible": False,
                    "image": None,
                }
                for _ in range(width)
            ]
            for _ in range(height)
        ]

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        else:
            raise IndexError("Cell out of bounds")

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["value"] = value
        else:
            raise IndexError("Cell out of bounds")
        
    def set_label(self, x, y, label):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["label"] = label
        else:
            raise IndexError("Cell out of bounds")

    def set_supercharged(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["supercharged"] = value
        else:
            raise IndexError("Cell out of bounds")

    def set_active(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["active"] = value
        else:
            raise IndexError("Cell out of bounds")

    def is_supercharged(self, x, y):
        return self.get_cell(x, y)["supercharged"]

    def set_adjacency_bonus(self, x, y, bonus):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["adjacency_bonus"] = bonus
        else:
            raise IndexError("Cell out of bounds")

    def set_bonus(self, x, y, bonus):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["bonus"] = bonus
        else:
            raise IndexError("Cell out of bounds")

    def set_type(self, x, y, type):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["type"] = type
        else:
            raise IndexError("Cell out of bounds")

    def set_value(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["value"] = value
        else:
            raise IndexError("Cell out of bounds")

    def set_total(self, x, y, total):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["total"] = total
        else:
            raise IndexError("Cell out of bounds")

    def set_module(self, x, y, module):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["module"] = module
        else:
            raise IndexError("Cell out of bounds")

    def set_adjacency(self, x, y, adjacency):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["adjacency"] = adjacency
        else:
            raise IndexError("Cell out of bounds")

    def set_tech(self, x, y, tech):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["tech"] = tech
        else:
            raise IndexError("Cell out of bounds")

    def set_sc_eligible(self, x, y, sc_eligible):
        """Set whether the cell at (x, y) is eligible for supercharging."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["sc_eligible"] = sc_eligible
        else:
            raise IndexError("Cell out of bounds")

    def set_image(self, x, y, image):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["image"] = image
        else:
            raise IndexError("Cell out of bounds")

    def to_dict(self):
        """Convert the grid into a JSON-serializable dictionary."""
        return {"width": self.width, "height": self.height, "cells": self.cells}

    @classmethod
    def from_dict(cls, data: dict) -> "Grid":
        """Create a Grid instance from a dictionary."""
        grid = cls(data["width"], data["height"])
        for y, row in enumerate(data["cells"]):
            for x, cell_data in enumerate(row):
                cell = grid.get_cell(x, y)
                cell.update(
                    {
                        "module": cell_data["module"],
                        "label": cell_data["label"],
                        "value": cell_data["value"],
                        "type": cell_data["type"],
                        "total": cell_data["total"],
                        "active": cell_data["active"],
                        "adjacency_bonus": cell_data["adjacency_bonus"],
                        "bonus": cell_data["bonus"],
                        "adjacency": cell_data["adjacency"],
                        "tech": cell_data["tech"],
                        "supercharged": cell_data["supercharged"],
                        "sc_eligible": cell_data["sc_eligible"],
                        "image": cell_data["image"],
                    }
                )
        return grid

    def __str__(self):
        """Generate a string representation of the grid."""
        return "\n".join(
            " ".join(
                "."
                if cell["value"] == 0
                else str(cell["total"])
                for cell in row
            )
            for row in self.cells
        )

def get_tech_modules(modules, ship, tech_key):
    """Retrieves modules for a specified ship and technology key, ignoring technology type."""
    ship_data = modules.get(ship)
    if ship_data is None:
        print(f"Error: Ship '{ship}' not found in modules data.")
        return None

    types_data = ship_data.get("types")
    if types_data is None:
        print(f"Error: 'types' key not found for ship '{ship}'.")
        return None

    for tech_type in types_data:
        tech_category = types_data.get(tech_type)
        if tech_category is None:
            print(f"Error: Technology type '{tech_type}' not found for ship '{ship}'.")
            continue #skip this type and check the next
        
        for technology in tech_category:
            if technology.get("key") == tech_key:
                modules_list = technology.get("modules")
                if modules_list is None:
                    print(f"Error: 'modules' key not found for technology '{tech_key}' within type '{tech_type}' on ship '{ship}'.")
                    return None
                return modules_list

    print(f"Error: Technology '{tech_key}' not found for ship '{ship}'.")
    return None

def get_tech_modules_for_training(modules, ship, tech_key):
    """Retrieves modules for training, returning the modules as they are in modules_refactored.py."""
    ship_data = modules.get(ship)
    if ship_data is None:
        print(f"Error: Ship '{ship}' not found in modules data.")
        return []

    types_data = ship_data.get("types")
    if types_data is None:
        print(f"Error: 'types' key not found for ship '{ship}'.")
        return []

    for tech_list in types_data.values():
        for tech_data in tech_list:
            if tech_data.get("key") == tech_key:
                return tech_data.get("modules", [])
    return []


def get_tech_tree_json(ship):
    """Generates a technology tree for a given ship and returns it as JSON."""
    try:
        tech_tree = get_tech_tree(ship)  # Call your existing function
        if "error" in tech_tree:
            return json.dumps({"error": tech_tree["error"]})  # Return error as JSON
        else:
            return json.dumps(tech_tree, indent=2)  # Return tree as JSON with indentation for readability
    except Exception as e:
        return json.dumps({"error": str(e)})  # Catch any errors during tree generation

def get_tech_tree(ship):
    """Generates a technology tree for a given ship."""
    ship_data = modules.get(ship)
    if ship_data is None:
        return {"error": f"Ship '{ship}' not found."}

    types_data = ship_data.get("types")
    if types_data is None:
        return {"error": f"'types' key not found for ship '{ship}'."}

    tech_tree = {}
    for tech_type, tech_list in types_data.items():
        tech_tree[tech_type] = []
        for tech in tech_list:
            tech_tree[tech_type].append(
                {
                    "label": tech["label"],
                    "key": tech["key"],
                    # Add other relevant fields if needed
                }
            )

    return tech_tree

def optimize_placement(grid, ship, modules, tech):
    # Initialize variables to store the optimal grid and the highest bonus found
    optimal_grid = None
    highest_bonus = 0.0
    iteration = 0

    # Retrieve the list of technology-specific modules for the given ship and tech
    tech_modules = get_tech_modules(modules, ship, tech)

    # Separate core and bonus modules from the list of tech modules
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]

    # Ensure there are both bonus and core modules available for placement
    if not core_modules:
        raise ValueError("No core modules specified")

    # Find all grid positions that are empty and active
    available_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if grid.get_cell(x, y)["module"] is None and grid.get_cell(x, y)["active"]
    ]

    # Iterate over every possible core module position
    for core_position in available_positions:
        # Generate all permutations of bonus module positions if there are bonus modules
        bonus_permutations = (
            [permutations(available_positions, len(bonus_modules))]
            if bonus_modules
            else [[]]
        )
        for bonus_placement in bonus_permutations[
            0
        ]:  # always loop at least once, even if empty.

            # Create a temporary grid to test the current configuration
            temp_grid = Grid.from_dict(grid.to_dict())  # Clone the grid

            # Place the core module at the specified position
            core_x, core_y = core_position
            core_module = core_modules[0]
            place_module(
                temp_grid,
                core_x,
                core_y,
                core_module["id"],
                core_module["label"],
                tech,
                core_module["type"],
                core_module["bonus"],
                core_module["adjacency"],
                core_module["sc_eligible"],
                core_module["image"],
            )

            # Place each bonus module at its respective position
            for index, bonus_position in enumerate(bonus_placement):
                x, y = bonus_position
                if temp_grid.get_cell(x, y)["module"] is not None:
                    continue
                bonus_module = bonus_modules[index]
                place_module(
                    temp_grid,
                    x,
                    y,
                    bonus_module["id"],
                    bonus_module["label"],
                    tech,
                    bonus_module["type"],
                    bonus_module["bonus"],
                    bonus_module["adjacency"],
                    bonus_module["sc_eligible"],
                    bonus_module["image"],
                )

            # Calculate adjacency bonuses and total bonuses for current grid configuration
            populate_adjacency_bonuses(temp_grid, tech)
            populate_module_bonuses(temp_grid, tech)
            core_bonus = populate_core_bonus(temp_grid, tech)

            # Update the optimal grid if the current configuration yields a higher bonus
            iteration += 1
            if core_bonus > highest_bonus:
                highest_bonus = core_bonus
                optimal_grid = Grid.from_dict(temp_grid.to_dict())  # Clone the temp grid

    # Return the grid configuration with the highest bonus and its bonus value
    return optimal_grid, highest_bonus

def simulated_annealing_optimization(
    grid,
    ship,
    modules,
    tech,
    initial_temp=100,
    cooling_rate=0.999,
    max_iterations=20000,
    patience=200,
    decay_factor=0.995,
    restart_probability=0.05,
    stagnation_threshold=1000,
    max_supercharged=4,
):
    """
    Performs simulated annealing optimization on a grid, but uses standard module IDs.

    Args:
        grid (Grid): The grid object to optimize.
        ship (str): The name of the ship.
        modules (dict): The global modules dictionary.
        tech (str): The key of the technology.
        initial_temp (float): Initial temperature for simulated annealing.
        cooling_rate (float): Cooling rate.
        max_iterations (int): Maximum number of iterations.
        patience (int): Patience for temperature decay.
        decay_factor (float): Factor by which temperature decays.
        restart_probability (float): Probability of random restart.
        stagnation_threshold (int): Threshold for stagnation restart.
        max_supercharged (int): Maximum number of supercharged slots.

    Returns:
        tuple: (best_grid, best_bonus)
            best_grid (Grid): The optimized grid.
            best_bonus (float): The best bonus score found.
    """
    best_grid = Grid.from_dict(grid.to_dict())
    best_bonus = -float("inf")
    current_grid = Grid.from_dict(grid.to_dict())
    temperature = initial_temp
    iteration_without_improvement = 0
    stagnation_counter = 0
    num_acceptances = 0
    total_iterations = 0

    for iteration in range(max_iterations):
        total_iterations += 1
        neighbor_grid = generate_neighbor_grid_with_movement(
            current_grid, modules, ship, tech, temperature, initial_temp, max_supercharged
        )

        if count_supercharged_slots(neighbor_grid, tech) > max_supercharged:
            continue

        populate_adjacency_bonuses(neighbor_grid, tech)
        populate_module_bonuses(neighbor_grid, tech)
        neighbor_bonus = populate_core_bonus(neighbor_grid, tech)

        if neighbor_bonus > best_bonus:
            best_bonus = neighbor_bonus
            best_grid = Grid.from_dict(neighbor_grid.to_dict())
            iteration_without_improvement = 0
            stagnation_counter = 0
            num_acceptances += 1
        else:
            iteration_without_improvement += 1
            stagnation_counter += 1

        energy_diff = neighbor_bonus - populate_core_bonus(current_grid, tech)

        if energy_diff < 0:
            acceptance_probability = math.exp(energy_diff / temperature)
            if random.random() < acceptance_probability:
                current_grid = Grid.from_dict(neighbor_grid.to_dict())
                num_acceptances += 1

        if iteration_without_improvement >= patience:
            temperature *= decay_factor
            iteration_without_improvement = 0

        temperature *= cooling_rate

        if stagnation_counter >= stagnation_threshold:
            if random.random() < restart_probability:
                current_grid = perturb_grid(best_grid, modules, ship, tech)
                temperature = initial_temp
                stagnation_counter = 0
                iteration_without_improvement = 0
            else:
                temperature = initial_temp
                stagnation_counter = 0

        # Print progress
        if iteration % 1000 == 0:
            print(
                f"simulated_annealing_optimization - tech: {tech} - Iteration {iteration}/{max_iterations}, Temp: {temperature:.2f}, Best Bonus: {best_bonus:.2f}, Cooling Rate: {cooling_rate:.4f}"
            )

    acceptance_rate = num_acceptances / total_iterations if total_iterations > 0 else 0
    print(f"Acceptance Rate: {acceptance_rate:.4f}")
    return best_grid, best_bonus

def generate_neighbor_grid_with_movement(
    grid, modules, ship, tech, temperature, initial_temp, max_supercharged
):
    neighbor_grid = Grid.from_dict(grid.to_dict())
    tech_modules = get_tech_modules(modules, ship, tech)
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]

    occupied_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if neighbor_grid.get_cell(x, y)["module"] is not None
    ]
    available_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if neighbor_grid.get_cell(x, y)["module"] is None
        and neighbor_grid.get_cell(x, y)["active"]
    ]
    supercharged_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if neighbor_grid.get_cell(x, y)["supercharged"]
    ]

    unoccupied_supercharged_positions = [
        pos for pos in supercharged_positions if pos not in occupied_positions
    ]

    move_count = max(1, int(5 * min(temperature / initial_temp, 1.0)))

    if not occupied_positions:
        # Prioritize supercharged slots for initial placement
        random.shuffle(unoccupied_supercharged_positions)
        for core_module in core_modules:
            if unoccupied_supercharged_positions:
                x, y = unoccupied_supercharged_positions.pop()
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    core_module["id"],
                    core_module["label"],
                    tech,
                    core_module["type"],
                    core_module["bonus"],
                    core_module["adjacency"],
                    core_module["sc_eligible"],
                    core_module["image"],
                )
            elif available_positions:
                x, y = random.choice(available_positions)
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    core_module["id"],
                    core_module["label"],
                    tech,
                    core_module["type"],
                    core_module["bonus"],
                    core_module["adjacency"],
                    core_module["sc_eligible"],
                    core_module["image"],
                )

        for bonus_module in bonus_modules:
            if (
                unoccupied_supercharged_positions
                and count_supercharged_slots(neighbor_grid, tech) < max_supercharged
            ):
                x, y = unoccupied_supercharged_positions.pop()
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    bonus_module["id"],
                    bonus_module["label"],
                    tech,
                    bonus_module["type"],
                    bonus_module["bonus"],
                    bonus_module["adjacency"],
                    bonus_module["sc_eligible"],
                    bonus_module["image"],
                )
            elif available_positions:
                x, y = random.choice(available_positions)
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    bonus_module["id"],
                    bonus_module["label"],
                    tech,
                    bonus_module["type"],
                    bonus_module["bonus"],
                    bonus_module["adjacency"],
                    bonus_module["sc_eligible"],
                    bonus_module["image"],
                )
    else:
        for _ in range(move_count):
            if not occupied_positions or not available_positions:
                break

            # Prioritize moving modules from non-supercharged positions if there are unoccupied supercharged slots
            if unoccupied_supercharged_positions:
                non_supercharged_occupied = [
                    pos
                    for pos in occupied_positions
                    if pos not in supercharged_positions
                ]
                if non_supercharged_occupied:
                    old_x, old_y = random.choice(non_supercharged_occupied)
                else:
                    old_x, old_y = random.choice(occupied_positions)
            else:
                old_x, old_y = random.choice(occupied_positions)

            occupied_positions.remove((old_x, old_y))
            old_cell = neighbor_grid.get_cell(old_x, old_y)
            old_module = old_cell["module"]

            # Clear the old cell before placing the module in a new location
            place_module(
                neighbor_grid, old_x, old_y, None, None, None, "", 0, False, False, None
            )

            # Prioritize moving to unoccupied supercharged positions
            if unoccupied_supercharged_positions:
                new_x, new_y = unoccupied_supercharged_positions.pop()
            else:
                # Find best available position based on adjacency
                new_x, new_y = find_best_available_position(
                    neighbor_grid, old_cell["tech"], available_positions
                )
                if (new_x, new_y) in available_positions:
                    available_positions.remove((new_x, new_y))

            # Enforce supercharged slot limit when placing a module
            is_supercharged = (
                old_cell["supercharged"]
                and count_supercharged_slots(neighbor_grid, tech) < max_supercharged
            )

            # Check if the cell is empty
            if neighbor_grid.get_cell(new_x, new_y)["module"] is None:
                place_module(
                    neighbor_grid,
                    new_x,
                    new_y,
                    old_module,
                    old_cell["label"],
                    old_cell["tech"],
                    old_cell["type"],
                    old_cell["bonus"],
                    old_cell["adjacency"],
                    is_supercharged,
                    old_cell["image"],
                )

    return neighbor_grid

def get_move_count(temperature, initial_temp):
    """
    Calculate the number of moves based on the current temperature.
    Use a square root function.
    """
    return max(1, int(10 * math.sqrt(temperature / initial_temp)))


def perturb_grid(grid, modules, ship, tech):
    """
    Introduce a significant perturbation to the grid. Uses standard module IDs.
    """
    perturbed_grid = Grid.from_dict(grid.to_dict())
    tech_modules = get_tech_modules_for_training(modules, ship, tech)
    available_positions = [
        (x, y)
        for y in range(perturbed_grid.height)
        for x in range(perturbed_grid.width)
        if perturbed_grid.get_cell(x, y)["module"] is None
    ]
    occupied_positions = [
        (x, y)
        for y in range(perturbed_grid.height)
        for x in range(perturbed_grid.width)
        if perturbed_grid.get_cell(x, y)["module"] is not None
    ]

    num_to_remove = int(0.5 * len(occupied_positions))
    if num_to_remove > 0:
        modules_to_relocate = random.sample(occupied_positions, num_to_remove)
        for x, y in modules_to_relocate:
            module_to_remove = perturbed_grid.get_cell(x, y)["module"]
            place_module(perturbed_grid, x, y, None, None, None, "", 0, False, False, None)
            available_positions.append((x,y))

        random.shuffle(available_positions)
        for x, y in modules_to_relocate:
            if available_positions:
                new_x, new_y = available_positions.pop()
                module_to_place = next((m for m in tech_modules if  m["id"] == module_to_remove), None) #changed here
                if module_to_place:
                    place_module(
                        perturbed_grid,
                        new_x,
                        new_y,
                        module_to_place["id"], #changed here
                        module_to_place["label"],
                        tech,
                        module_to_place["type"],
                        module_to_place["bonus"],
                        module_to_place["adjacency"],
                        module_to_place["sc_eligible"],
                        module_to_place["image"],
                    )
                else:
                    print(
                        f"Warning: Module with id {module_to_remove} not found in tech_modules. Available keys: {list(tech_modules[0].keys()) if tech_modules else []}"
                    )

    return perturbed_grid

def find_best_available_position(grid, tech, available_positions):
    best_position = None
    max_weighted_score = -1

    for x, y in available_positions:
        adjacency_bonus = calculate_potential_adjacency_bonus(grid, x, y, tech)
        is_supercharged = grid.get_cell(x, y)["supercharged"]

        # Weighted score: Prioritizes adjacency, then supercharged slots
        weighted_score = (adjacency_bonus * 2) + (0.25 if is_supercharged else 0) # Adjust weights as needed

        if weighted_score > max_weighted_score:
            max_weighted_score = weighted_score
            best_position = (x, y)

    return best_position if best_position else random.choice(available_positions)

def calculate_potential_adjacency_bonus(grid, x, y, tech):
    """Calculate the potential adjacency bonus if a module were placed at (x, y)."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    adjacency_bonus = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.width and 0 <= ny < grid.height:
            neighbor = grid.get_cell(nx, ny)
            if neighbor["module"] is not None and neighbor["tech"] == tech:
                adjacency_bonus += 1
    return adjacency_bonus


def count_supercharged_slots(grid, tech):
    count = 0
    for y in range(grid.height):
        for x in range(grid.width):
            if (
                grid.get_cell(x, y)["supercharged"]
                and grid.get_cell(x, y)["tech"] == tech
            ):
                count += 1
    return count


def place_module(grid, x, y, module, label, tech, type, bonus, adjacency, sc_eligible, image):
    grid.set_module(x, y, module)
    grid.set_label(x, y, label)
    grid.set_tech(x, y, tech)
    grid.set_type(x, y, type)
    grid.set_bonus(x, y, bonus)
    grid.set_adjacency(x, y, adjacency)
    grid.set_sc_eligible(x, y, sc_eligible)
    grid.set_image(x, y, image)

def calculate_adjacency_bonus(grid, x, y):
    cell = grid.get_cell(x, y)
    if not cell["adjacency"]:
        return 0.0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Only orthogonal directions
    adjacency_bonus = 0.0

    # Trying a different approach
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.width and 0 <= ny < grid.height:
            neighbor = grid.get_cell(nx, ny)
            if neighbor["module"] is not None and neighbor["tech"] == cell["tech"]:
                adjacency_bonus += 1
                grid.set_adjacency_bonus(x, y, adjacency_bonus)

    return adjacency_bonus


def populate_adjacency_bonuses(grid, tech):
    for row in range(grid.height):
        for col in range(grid.width):
            current_cell = grid.get_cell(col, row)
            if current_cell["module"] is not None and current_cell["tech"] == tech:
                calculate_adjacency_bonus(grid, col, row)


def calculate_module_bonus(grid, x, y):
    cell = grid.get_cell(x, y)

    base_bonus = cell["bonus"]
    adjacency_bonus = cell["adjacency_bonus"]
    is_supercharged = cell["supercharged"]
    is_sc_eligible = cell["sc_eligible"]

    total_bonus = base_bonus * adjacency_bonus

    if is_supercharged & is_sc_eligible == True:
        total_bonus *= 1.25

    grid.set_total(x, y, total_bonus)
    return total_bonus


def populate_module_bonuses(grid, tech):
    for row in range(grid.height):
        for col in range(grid.width):
            current_cell = grid.get_cell(col, row)
            if current_cell["type"] == "bonus" and current_cell["tech"] == tech:
                calculate_module_bonus(grid, col, row)


def calculate_core_bonus(grid, tech):
    """
    Calculate the core bonus by summing the total bonus of all bonus modules and adding in the core module's total.
    """
    bonus_total = 0
    core_total = 0

    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(col, row)
            if cell["type"] == "bonus" and cell["tech"] == tech:
                bonus_total += cell["total"] * cell["adjacency_bonus"]
            elif cell["type"] == "core" and cell["tech"] == tech:
                core_total = cell["bonus"] + cell["adjacency_bonus"]

    return bonus_total + core_total

def populate_core_bonus(grid, tech):
    core_bonus = calculate_core_bonus(grid, tech)
    final_bonus = 0
    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(col, row)
            if cell["type"] == "core" and cell["tech"] == tech:
                if cell["sc_eligible"] and cell["supercharged"]:
                    final_bonus = core_bonus * 1.25  # Apply bonus if supercharged
                else:
                    final_bonus = core_bonus
                grid.set_total(col, row, final_bonus)

    return final_bonus


def print_grid(grid):
    """Display the grid with module info, total value, and active state (+/-) instead of '.'."""
    # Format and print the grid
    for y, row in enumerate(grid.cells):
        formatted_row = []

        for x, cell in enumerate(row):
            cell_data = copy.deepcopy(
                grid.get_cell(x, y)
            )  # make a copy of the data to ensure we don't modify it
            is_supercharged = cell_data["supercharged"]
            is_shield = cell_data["tech"] == "shield"
            is_infra = cell_data["tech"] == "infra"
            active_state = (
                " +" if cell_data["active"] else " -"
            )  # what to show if there is no module

            formatted_row.append(
                f"\033[93m{active_state if cell_data['module'] is None else cell_data['module']} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                if is_supercharged
                else (
                    f"\033[96m{active_state if cell_data['module'] is None else cell_data['module']} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                    if is_shield
                    else (
                        f"\033[91m{active_state if cell_data['module'] is None else cell_data['module']} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                        if is_infra
                        else f"{active_state if cell_data['module'] is None else cell_data['module']} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})"
                    )
                )
            )
        print(" | ".join(formatted_row))
    print()
    
def print_grid_compact(grid):
    """Display the grid with module info, total value, and active state (+/-) instead of '.'."""
    # Format and print the grid
    for y, row in enumerate(grid.cells):
        formatted_row = []

        for x, cell in enumerate(row):
            cell_data = copy.deepcopy(
                grid.get_cell(x, y)
            )  # make a copy of the data to ensure we don't modify it
            is_supercharged = cell_data["supercharged"]
            is_shield = cell_data["tech"] == "shield"
            is_infra = cell_data["tech"] == "infra"
            active_state = (
                " +" if cell_data["active"] else " -"
            )  # what to show if there is no module

            formatted_row.append(
                f"\033[93m{active_state if cell_data['module'] is None else cell_data['module']} \033[0m"
                if is_supercharged
                else (
                    f"\033[96m{active_state if cell_data['module'] is None else cell_data['module']} \033[0m"
                    if is_shield
                    else (
                        f"\033[91m{active_state if cell_data['module'] is None else cell_data['module']} \033[0m"
                        if is_infra
                        else f"{active_state if cell_data['module'] is None else cell_data['module']} "
                    )
                )
            )
        print(" | ".join(formatted_row))
    print()