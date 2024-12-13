import sys
import os
from io import StringIO
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Classes.Grid import Grid
from Backend.Utilities.Utils import upload_manifest
from Backend.Classes.Pathfinder import Pathfinder
from unittest.mock import patch


@pytest.fixture
def pathfinder():
    # Load the manifest for ShipCase1
    manifest_data = upload_manifest("ShipCase1.txt")
    grid = Grid()
    grid.setup_grid(manifest_data)
    return Pathfinder(grid)


@pytest.fixture
def pathfinder(shipcase):
    # Load the manifest for the given shipcase
    manifest_data = upload_manifest(f"ShipCase{shipcase}.txt")
    grid = Grid()
    grid.setup_grid(manifest_data)
    return Pathfinder(grid)


@pytest.mark.parametrize("shipcase", [1, 2, 3, 4, 6])  # Adding ShipCase3
def test_balancing_move_prints(shipcase, pathfinder, capsys):
    expected_balance_moves = {
        1: [
            "Move container from position (0, 2) to position (0, 6), Time estimation: 14 minutes",
            "Move crane from position (0, 6) to position (8, 0), Time estimation: 14 minutes"
        ],
        2: [
            "Move container from position (0, 3) to position (0, 6), Time estimation: 14 minutes",
            "Move container from position (0, 8) to position (0, 5), Time estimation: 7 minutes"
            "Move crane from position (0, 5) to position (8, 0), Time estimation: 13 minutes"
        ],
        3: [
            "Move container from position (1, 0) to position (2, 1), Time estimation: 9 minutes",
            "Move container from position (0, 0) to position (0, 6), Time estimation: 15 minutes",
            "Move crane from position (0, 6) to position (8, 0), Time estimation: 14 minutes"
        ],
        4: [
            "Move container from position (7, 4) to position (1, 3), Time estimation: 12 minutes",
            "Move container from position (6, 4) to position (1, 6), Time estimation: 13 minutes",
            "Move container from position (5, 4) to position (2, 3), Time estimation: 10 minutes",
            "Move container from position (4, 4) to position (2, 6), Time estimation: 7 minutes"
            "Move crane from position (2, 6) to position (8, 0), Time estimation: 12 minutes"
        ],
        6: [
            "Move container from position (1, 1) to position (1, 0), Time estimation: 9 minutes",
            "Move container from position (0, 1) to position (0, 6), Time estimation: 9 minutes",
            "Move crane from position (0, 6) to position (8, 0), Time estimation: 14 minutes"
        ]
    }
    
    expected_moves = expected_balance_moves[shipcase]
    
    with patch('builtins.input', return_value='1'):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            balance_moves = pathfinder.balance()
            for move in balance_moves:
                print(move) 

            output = mock_stdout.getvalue()

    actual_moves = output.strip().split('\n') 
    
    assert actual_moves == expected_moves, f"Expected moves for ShipCase{shipcase}: {expected_moves}, but got: {actual_moves}"