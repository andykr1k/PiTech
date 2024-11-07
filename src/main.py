import os
from models.grid import Grid

def upload_manifest(file_name):
    path = f'../manifests/{file_name}'
    if not os.path.exists(path):
        print(f"Manifest '{file_name}' not found.")
        return None
    with open(path, 'r') as manifest_file:
        return manifest_file.readlines()
    
def upload_transfer_list(file_name):
    path = f'../transferlist/{file_name}'
    if not os.path.exists(path):
        print(f"Transfer List '{file_name}' not found.")
        return None
    with open(path, 'r') as transfer_list:
        return transfer_list.readlines()
    

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
        
        new_grid = Grid()
        new_grid.setup_grid(manifest_data)
        
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