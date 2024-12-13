from Backend.Classes.Grid import Grid
from Backend.Utilities.Utils import upload_manifest, upload_transfer_list
from Backend.Classes.Pathfinder import Pathfinder
import time
import signal

# Timeout exception class
class TimeoutException(Exception):
    pass

# Timeout handler
def timeout_handler(signum, frame):
    raise TimeoutException
timeout_duration = 900  # 10 minutes
test_cases2 = [f"{i}Containers.txt" for i in range(41, 51)]  # Generate filenames dynamically

# Iterate through balancing test cases
for manifest_name in test_cases2:
    try:
        # Set the timeout handler
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_duration)  # Start the timeout clock

        manifest_data = upload_manifest(manifest_name)

        new_grid = Grid()
        new_grid.setup_grid(manifest_data)
        pathfinder = Pathfinder(new_grid)

        print(f"Balancing job selected for {manifest_name}.")
        start_time = time.time()

        # Run the balance function
        balance_moves = pathfinder.balance()

        end_time = time.time()
        cost_time = end_time - start_time

        # Display results
        print(f"\nBalance Moves for {manifest_name}:")
        for move in balance_moves:
            print(move[0])
        print(f"\nBalancing for {manifest_name} completed in {cost_time:.1f} seconds.")
        print("=" * 40)

    except TimeoutException:
        print(f"\nBalancing for {manifest_name} exceeded 10 minutes and was skipped.")
        print("=" * 40)

    finally:
        signal.alarm(0)  # Disable the alarm for the next test