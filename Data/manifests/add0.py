import os

def add_zero_to_row_index(input_file, output_file):
    """
    Reads a file, adds leading zeros to row indices, and writes the output to a new file.
    
    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Match the format [row,col]
            if line.startswith("[") and "," in line:
                parts = line.split("]", 1)
                row_col = parts[0][1:]  # Extract row and column e.g., "1,01"
                row, col = row_col.split(",")
                new_row = row.zfill(2)  # Add leading zero to the row
                updated_line = f"[{new_row},{col}]{parts[1]}"
                outfile.write(updated_line)
            else:
                outfile.write(line)  # Write other lines unchanged

# Process files from 20 to 89
for i in range(20, 89):
    input_file = f"{i}Containers.txt"
    temp_file = f"{i}Containers_temp.txt"  # Temporary file for writing

    try:
        # Process the file and write to a temporary file
        add_zero_to_row_index(input_file, temp_file)
        
        # Replace the original file with the processed file
        os.replace(temp_file, input_file)
        print(f"Processed: {input_file}")
    except FileNotFoundError:
        print(f"File not found: {input_file}, skipping...")
    except Exception as e:
        print(f"An error occurred with {input_file}: {e}")
