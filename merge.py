import json
import os
import re

# Directories to traverse
directories = ['base', 'dlc', 'update', 'retro']

# Dictionary to store the combined data
combined_data = {"titledb": {}}

def sanitize_text(text):
    if text is None:
        return ""  # Return an empty string if the text is None

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
    # Add automatic line breaks
    text = add_line_breaks(text, max_length=80)
    return text.strip()

def add_line_breaks(text, max_length):
    lines = []
    for paragraph in text.split('\n'):
        line = ''
        for word in paragraph.split(' '):
            if len(line) + len(word) + 1 > max_length:
                lines.append(line)
                line = word
            else:
                if line:
                    line += ' '
                line += word
        lines.append(line)
    return '\n'.join(lines)

# Traverse each directory
for directory in directories:
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    game_data = json.load(f)
                    game_id = game_data["id"]
                    
                    # Sanitize the description field if it exists and is not None
                    if "description" in game_data and game_data["description"] is not None:
                        game_data["description"] = sanitize_text(game_data["description"])
                    
                    combined_data["titledb"][game_id] = game_data

# Write the combined data to fulldb.json
with open('fulldb.json', 'w', encoding='utf-8') as outfile:
    json.dump(combined_data, outfile, indent=4)

print("fulldb.json has been created successfully.")
