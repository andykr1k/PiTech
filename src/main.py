import os
from models.grid_balance import GridState
from pathfinder.balance import Balance_Problem

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
        
        if job_choice == '1':
            print("Balancing job selected.")
            grid = GridState(rows=6, columns=8)
            
            #grid.setup_grid("../manifests/sample_manifest_notbalanced.txt") #size 6x8 can't be balanced
            grid.setup_grid("../manifests/sample_manifest_balanced.txt") #size 6x8 already balanced
            #grid.setup_grid("../manifests/sample_manifest_children_test_1.txt") #size 4x6 can be balanced
            print(grid.goal_weight)
            problem = Balance_Problem(grid)
            problem.solve()
        
        elif job_choice == '2':
            print("Transferring job selected.")
        
        else:
            print("Invalid input. Please try again.")
        
        print("=" * 40)
        
if __name__ == "__main__":
    main()