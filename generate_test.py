import random

def generate_grid(num_containers=40):
    rows, cols = 8, 11  # Grid dimensions (8 rows, 11 columns)
    grid = [["UNUSED" for _ in range(cols)] for _ in range(rows)]

    # Predefined container names
    container_names = [
        "Orion", "Tesla", "Neptune", "Apollo", "Horizon", "Atlas", "Ember",
        "Zenith", "Nova", "Echo", "Phoenix", "Quantum", "Solstice", "Mirage",
        "Everest", "Polaris", "Halo", "Comet", "Eclipse", "Glacier", "Inferno",
        "Twilight", "Gravity", "Odyssey", "Nimbus", "Velocity", "Stardust",
        "Titan", "Voyager", "Cosmos", "Echo", "Cyclone", "Zenith", "Zephyr",
        "Aurora", "Blaze", "Meteor", "Spectrum", "Lunar", "Vortex", "Spectrum",
        "Matrix", "Aero", "Prism", "Vertex", "Nexus", "Eclipse", "Shadow",
        "Drift", "Infinity", "Singularity", "Zenith", "Sol", "Horizon", "Glider",
        "Arcadia", "Shard", "Radiance", "Dynamo", "Tectonic", "Axis", "Vertex",
        "Beacon", "Crystal", "Circuit", "Velocity", "Cascade", "Forge", "Spectrum",
        "Borealis"
    ]

    # Place containers
    remaining_containers = num_containers
    while remaining_containers > 0:
        col = random.randint(0, cols - 1)  # Randomly select a column

        # Find the first available row from the bottom (index 0 to index 7)
        for row in range(rows):  # Start from index 0 (row 1) and move upward
            if grid[row][col] == "UNUSED":  # Place container here
                weight = random.randint(100, 1000)  # Random weight
                name = random.choice(container_names)
                grid[row][col] = f"{{{weight:05}}}, {name}"  # Format weight as 5 digits
                remaining_containers -= 1
                break

    # Format grid as output
    formatted_grid = []
    for row in range(rows):  # Output starts from bottom row (index 0)
        for col in range(cols):
            position = f"[{row + 1},{col + 1:02}]"  # Convert to 1-based indexing
            if grid[row][col] == "UNUSED":
                formatted_grid.append(f"{position}, {{00000}}, UNUSED")
            else:
                formatted_grid.append(f"{position}, {grid[row][col]}")

    return formatted_grid

# Generate and save the grid
for i in range(41, 90):  # Generate grids for 21 to 30 containers
    test_grid = generate_grid(num_containers=i)
    filename = f"{i}Containers.txt"  # Use f-string to format the filename
    with open(filename, "w") as file:
        for line in test_grid:
            file.write(line + "\n")

