from Backend.Classes.Grid import Grid
from Backend.Utilities.Utils import upload_manifest
from Backend.Utilities.Utils import upload_transfer_list
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
        
        manifest_name = "ShipCase4.txt"
        manifest_data = upload_manifest(manifest_name)
        

        
        if job_choice == '1':
            new_grid = Grid()
            new_grid.setup_grid(manifest_data)
            pathfinder = Pathfinder(new_grid)
        
            print("Balancing job selected.")
            balance_moves = pathfinder.balance()
            print('Balance Moves:')
            for move in balance_moves:
                print(move)
        
        elif job_choice == '2':
            transfer_name = "case4.txt"
            transfer_data = upload_transfer_list(transfer_name)
        
            new_grid = Grid()
            new_grid.setup_grid(manifest_data)
            new_grid.setup_transferlist(transfer_data)
            
            print("Transferring job selected.")
            transfer_moves = pathfinder.transfer()
            print('Transfer Moves:')
            
            for move in transfer_moves:
                print(move)
            
        else:
            print("Invalid input. Please try again.")
        
        print("=" * 40)
        
if __name__ == "__main__":
    main()