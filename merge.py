import json
import os

# Directories to traverse
directories = ['base', 'dlc', 'update', 'forwarder']

# Dictionary to store the combined data
combined_data = {"titledb": {}}

# Traverse each directory
for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                game_data = json.load(f)
                game_id = game_data["id"]
                combined_data["titledb"][game_id] = game_data

# Write the combined data to fulldb.json
with open('fulldb.json', 'w') as outfile:
    json.dump(combined_data, outfile, indent=4)

print("fulldb.json has been created successfully.")
