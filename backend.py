from Backend.Classes.Grid import Grid
from Backend.Utilities.Utils import upload_manifest
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

        new_grid = Grid()
        new_grid.setup_grid(manifest_data)
        #print(new_grid)

        pathfinder = Pathfinder(new_grid)
        
        if job_choice == '1':
            print("Balancing job selected.")
            balance_moves = pathfinder.balance()
            print('Balance Moves:')
            for move in balance_moves:
                print(move)
            
            
        
        # elif job_choice == '2':
        #     print("Transferring job selected.")
        #     transfer_list_name = "sample_transfer_list.txt"
        #     transfer_list = upload_transfer_list(transfer_list_name)
            
        else:
            print("Invalid input. Please try again.")
        
        print("=" * 40)
        
if __name__ == "__main__":
    main()