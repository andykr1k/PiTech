import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Classes.GridState import GridState
from Utilities.Utils import upload_manifest

grid = GridState(rows=6, columns=8)

manifest_name = "sample_manifest.txt"
manifest_data = upload_manifest(manifest_name)
grid.setup_grid(manifest_data)

print(grid)

x, y, z = grid.calculate_weights()
print(f"Weight: {x, y, z}")
print(f"Is_balanced: {grid.isBalanced()}")

#check get_movable_containers_position
position = grid.get_movable_containers_position()
position_display = [(i + 1, j + 1) for i, j in position]
print(f"Available container to move: {position_display}")

#check get_valid_slots_position
slots = grid.get_valid_slots_position((3,1))
slots_display = [(i + 1, j + 1) for i, j in slots]
print(f"Available slots to move container (3, 1): {slots_display}")

children = grid.expand()
print(f"Numbers of children: {len(children)}")