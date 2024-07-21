import json
import os
import re  # Ensure this import statement is present

# Directories to traverse
directories = ['base', 'dlc', 'update', 'retro']

# Dictionary to store the combined data
combined_data = {"titledb": {}}

def sanitize_text(text):
    # Replace <br> and <br/> with spaces
    text = text.replace('<br>', ' ').replace('<br/>', ' ')
    # Remove any other HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Replace specific characters with Unicode escape sequences
    unicode_replacements = {
        '…': '\\u2026',
        '‘': '\\u2018',
        '’': '\\u2019',
        '“': '\\u201C',
        '”': '\\u201D',
        '—': '\\u2014',
        '–': '\\u2013',
        ' ': '\\u00A0',  # Non-breaking space
        'é': '\\u00E9',
        'à': '\\u00E0',
        'è': '\\u00E8',
        'ê': '\\u00EA',
        'ç': '\\u00E7',
        'ô': '\\u00F4',
        'û': '\\u00FB',
        'ù': '\\u00F9',
        'î': '\\u00EE',
        'ï': '\\u00EF',
        'â': '\\u00E2',
        'ä': '\\u00E4',
        'ë': '\\u00EB',
        'ö': '\\u00F6',
        'ü': '\\u00FC',
        'œ': '\\u0153'
    }
    for char, replacement in unicode_replacements.items():
        text = text.replace(char, replacement)
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
    json.dump(combined_data, outfile, indent=4, ensure_ascii=False)

print("fulldb.json has been created successfully.")
