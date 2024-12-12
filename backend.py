from Backend.Classes.Grid import Grid
from Backend.Utilities.Utils import upload_manifest, upload_transfer_list
from Backend.Classes.Pathfinder import Pathfinder

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
        
        # Loop through ShipCase1 to ShipCase6
        # Load manifest for the current shipcase (ShipCase1, ShipCase2, ...)
        manifest_name = "ShipCase2.txt"
        #i = 6
        #manifest_name = f"ShipCase{i}.txt"
        manifest_data = upload_manifest(manifest_name)
        
        if job_choice == '1':  # Balancing job
            new_grid = Grid(id="Main_Grid")
            new_grid.setup_grid(manifest_data)
            pathfinder = Pathfinder(new_grid)
            
            print(f"Balancing job selected for {manifest_name}.")
            balance_moves = pathfinder.balance()
            print('Balance Moves:')
            print(balance_moves)
            for move in balance_moves:
                print(move)
            
        elif job_choice == '2':  # Transferring job
            # Load transfer list for the current case (Case1, Case2, ...)
            transfer_name = f"Case2.txt"
            transfer_data = upload_transfer_list(transfer_name)
            
            new_grid = Grid(id="Main_Grid")
            new_grid.setup_grid(manifest_data)
            new_grid.setup_transferlist(transfer_data)
            pathfinder = Pathfinder(new_grid)
                
            print(f"Transferring job selected for {manifest_name}.")
            transfer_moves = pathfinder.transfer()
            print('Transfer Moves:')
            
            for move in transfer_moves:
                print(move)
            
        else:
            print("Invalid input. Please try again.")
        
        print("=" * 40)

if __name__ == "__main__":
    main()
