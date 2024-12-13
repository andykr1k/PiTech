from Backend.Classes.Grid import Grid
from Backend.Utilities.Utils import upload_manifest, upload_transfer_list
from Backend.Classes.Pathfinder import Pathfinder
import time 

def main():
    while True:
        print("Please select a job:")
        print("1. Balancing")
        print("2. Transferring")
        print("q for Quit")
        job_choice = input("Enter the number for your job selection: ")
        print("=" * 40)
        
        if job_choice == 'q':
            print("Quitting program.")
            break
        
        i = 4
        manifest_name = f"ShipCase{i}.txt"
        manifest_data = upload_manifest(manifest_name)
        
        if job_choice == '1':  # Balancing job
            
            new_grid = Grid()
            new_grid.setup_grid(manifest_data)
            pathfinder = Pathfinder(new_grid)
            
            print(f"Balancing job selected for {manifest_name}.")
            start_time = time.time()
            
            balance_moves = pathfinder.balance()
            
            end_time = time.time()
            cost_time = end_time - start_time
            
            print('Balance Moves:')
            for move in balance_moves:
                print(move[0])
            print(f"\nBalancing completed in {cost_time:.1f} seconds.")
            
        elif job_choice == '2':  # Transferring job
            # Load transfer list for the current case (Case1, Case2, ...)
            transfer_name = f"Case{i}.txt"
            transfer_data = upload_transfer_list(transfer_name)
            
            new_grid = Grid()
            new_grid.setup_grid(manifest_data)
            new_grid.setup_transferlist(transfer_data)
            pathfinder = Pathfinder(new_grid)
                
            print(f"Transferring job selected for {manifest_name}.")
            transfer_moves = pathfinder.transfer()
            print('Transfer Moves:')
            
            for move in transfer_moves:
                print(move[0])
                
        
        else:
            print("Invalid input. Please try again.")
        
        print("=" * 40)

if __name__ == "__main__":
    main()
