import sys
import os
from io import StringIO
import pytest
from unittest.mock import patch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Classes.Grid import Grid
from Backend.Utilities.Utils import upload_manifest, upload_transfer_list
from Backend.Classes.Pathfinder import Pathfinder

@pytest.fixture
def pathfinder_with_transfer(shipcase):
    # Load the manifest and transfer list for the given shipcase
    manifest_data = upload_manifest(f"ShipCase{shipcase}.txt")
    transfer_data = upload_transfer_list(f"Case{shipcase}.txt")  # Assuming transfer lists are named Case1.txt, Case2.txt, etc.
    
    grid = Grid()
    grid.setup_grid(manifest_data)
    grid.setup_transferlist(transfer_data)
    
    return Pathfinder(grid)


# Test case to simulate the Transfer job selection for ShipCase1 to ShipCase6
@pytest.mark.parametrize("shipcase", [1, 2, 3, 4, 5, 6])  # Adding ShipCase1 to ShipCase6
def test_transfer_move_prints(shipcase, pathfinder_with_transfer, capsys):
    expected_transfer_moves = {
        1: [
            "Move container from position (0, 1) to position truck, Time estimation: 20 minutes",
            "Move crane from position truck to position (8, 0), Time estimation: 2 minutes"
        ],
        2: [
            "Move container from position truck to position (3, 0), Time estimation: 9 minutes",
            "Move crane from position (3, 0) to position (8, 0), Time estimation: 5 minutes"
        ],
        3: [
            "Move container from position truck to position (2, 0), Time estimation: 10 minutes",
            "Move container from position (1, 1) to position (1, 2), Time estimation: 3 minutes",
            "Move container from position (0, 1) to position truck, Time estimation: 13 minutes",
            "Move container from position truck to position (3, 0), Time estimation: 7 minutes",
            "Move crane from position (3, 0) to position (8, 0), Time estimation: 5 minutes"
        ],
        4: [
            "Move container from position (7, 4) to position (1, 5), Time estimation: 12 minutes",
            "Move container from position (6, 4) to position truck, Time estimation: 14 minutes",
            "Move container from position truck to position (6, 4), Time estimation: 8 minutes",
            "Move crane from position (6, 4) to position (8, 0), Time estimation: 6 minutes"
        ],
        5: [
            "Move container from position truck to position (1, 0), Time estimation: 11 minutes",
            "Move container from position (0, 3) to position truck, Time estimation: 17 minutes",
            "Move container from position truck to position (2, 0), Time estimation: 8 minutes",
            "Move container from position (0, 4) to position truck, Time estimation: 20 minutes",
            "Move crane from position truck to position (8, 0), Time estimation: 2 minutes"
        ],
        6: [
            "Move container from position truck to position (1, 0), Time estimation: 11 minutes",
            "Move container from position (1, 1) to position (1, 2), Time estimation: 2 minutes",
            "Move container from position (0, 3) to position truck, Time estimation: 15 minutes",
            "Move container from position (0, 1) to position truck, Time estimation: 22 minutes",
            "Move crane from position truck to position (8, 0), Time estimation: 2 minutes"
         ],
    }

    expected_moves = expected_transfer_moves[shipcase]

    with patch('builtins.input', return_value='2'):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            transfer_moves = pathfinder_with_transfer.transfer()
            for move in transfer_moves:
                print(move)  # Only printing the moves
            output = mock_stdout.getvalue()

    actual_moves = output.strip().split('\n')  # Get each printed move as a list

    assert actual_moves == expected_moves, f"Expected moves for ShipCase{shipcase}: {expected_moves}, but got: {actual_moves}"