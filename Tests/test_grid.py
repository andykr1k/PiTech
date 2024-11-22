import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Classes.Grid import Grid
from Backend.Classes.Slot import Slot
from Backend.Utilities.Utils import upload_manifest


@pytest.fixture
def manifest_data():
    manifest_name = "sample_manifest.txt"
    return upload_manifest(manifest_name)

@pytest.fixture
def grid(manifest_data):
    grid = Grid(8, 12)
    grid.setup_grid(manifest_data)
    return grid


def test_grid_initialization(grid):
    assert grid.rows == 8
    assert grid.columns == 12

def test_upload_manifest(manifest_data):
    assert manifest_data is not None
    assert isinstance(manifest_data, list)

def test_grid_setup(grid):
    print(grid)
    print(f'slot print test: {grid.slot[0][1]}')
    assert grid.slot[0][0] is not None 


def test_move_container(grid):
    initial_slot = grid.slot[0][0]
    target_slot = grid.slot[1][1]
    
    # Assuming move_container is a method in Grid class
    grid.move_container(initial_slot, target_slot)
    assert target_slot.container is not None
    assert initial_slot.container is None

def test_get_movable_containers_position(grid):
    #figure out the list of movable containers positions
    #assert that the list returned is the same list as mine
    pass

def test_add_container_to_slot(grid):
    pass

def test_remove_container_from_slot(grid):
    pass

def test_find_container_by_id(grid):
    pass

def test_get_container_position(grid):
    pass

def test_is_slot_empty(grid):
    pass

def test_get_adjacent_slots(grid):
    pass

def test_save_grid_state(grid):
    pass

def test_load_grid_state(grid):
    pass
if __name__ == "__main__":
    pytest.main()