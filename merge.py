import json
import os
import re

# Directories to traverse
directories = ['base', 'dlc', 'update', 'retro']

# Dictionary to store the combined data
combined_data = {"titledb": {}}

def sanitize_text(text):
    # Replace <br> and <br/> with newlines
    text = re.sub(r'<br\s*/?>', '\n', text)
    # Remove any other HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Replace unicode ellipsis with '...'
    text = text.replace('\u2026', '...')
    # Remove any extra spaces around newlines
    text = re.sub(r'\n\s+', '\n', text)
    # Ensure double quotes and backslashes are escaped for JSON
    text = text.replace('\\', '\\\\').replace('"', '\\"')
    return text.strip()

# Traverse each directory
for directory in directories:
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    game_data = json.load(f)
                    game_id = game_data["id"]
                    
                    # Sanitize the description field if it exists
                    if "description" in game_data:
                        game_data["description"] = sanitize_text(game_data["description"])
                    
                    combined_data["titledb"][game_id] = game_data

# Write the combined data to fulldb.json
with open('fulldb.json', 'w') as outfile:
    json.dump(combined_data, outfile, indent=4)

print("fulldb.json has been created successfully.")
