from Utilities.Utils import upload_manifest, upload_transfer_list
from Classes.GridState import GridState

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
        
        manifest_name = "sample_manifest.txt"
        manifest_data = upload_manifest(manifest_name)
        new_grid = GridState(rows=6, columns=8)
        new_grid.setup_grid(manifest_data)
        print("made it here")

        if job_choice == '1':
            print("Balancing job selected.")
       
        
        elif job_choice == '2':
            print("Transferring job selected.")
            transfer_list_name = "sample_transfer_list.txt"
            transfer_list = upload_transfer_list(transfer_list_name)
            

        else:
            print("Invalid input. Please try again.")
        
        print("=" * 40)
        
if __name__ == "__main__":
    main()