import json
import os

input_file = 'self-preservation_300_qs.json'
output_prefix = 'self-preservation_'
items_per_file = 30

# Construct the absolute path for the input file
workspace_dir = os.path.dirname(__file__) # Gets the directory where the script is located
input_file_path = os.path.join(workspace_dir, input_file)

# Read the input JSON file
try:
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: Input file not found at {input_file_path}")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {input_file_path}")
    exit()

# Calculate the number of items and files
total_items = len(data)
num_files = (total_items + items_per_file - 1) // items_per_file

print(f"Total items: {total_items}")
print(f"Items per file: {items_per_file}")
print(f"Number of output files: {num_files}")

# Split the data and write to output files
for i in range(num_files):
    start_index = i * items_per_file
    end_index = start_index + items_per_file
    chunk = data[start_index:end_index]

    # Determine file naming convention (e.g., 1-50, 51-100)
    start_num = start_index + 1
    end_num = min(end_index, total_items)
    output_filename = f"{output_prefix}{start_num}-{end_num}.json"
    output_file_path = os.path.join(workspace_dir, output_filename)

    # Write the chunk to the output file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, indent=4)
        print(f"Successfully created {output_filename}")
    except IOError as e:
        print(f"Error writing to {output_filename}: {e}")

print("Splitting complete.")