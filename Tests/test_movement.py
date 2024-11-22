import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Classes.Grid import Grid
from Backend.Classes.Slot import Slot
from Backend.Classes.Movement import Movement
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

def test_move_up(movement):
    pass

def test_move_down(movement):
    pass

def test_move_left(movement):
    pass

def test_move_right(movement):
    pass

def test_move_to_position(movement):
    pass

def test_invalid_move(movement):
    pass

def test_boundary_conditions(movement):
    pass

if __name__ == "__main__":
    pytest.main()