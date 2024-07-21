import json
import os

def get_missing_info_fields(game_details):
    """Returns a list of fields that are missing or have invalid values."""
    missing_fields = []
    
    if 'description' not in game_details or not game_details['description']:
        missing_fields.append('description')
    if 'name' not in game_details or not game_details['name']:
        missing_fields.append('name')
    if 'publisher' not in game_details or not game_details['publisher']:
        missing_fields.append('publisher')
    if 'region' not in game_details or not game_details['region']:
        missing_fields.append('region')
    if 'releaseDate' not in game_details or not isinstance(game_details['releaseDate'], int):
        missing_fields.append('releaseDate')
    if 'size' not in game_details or not isinstance(game_details['size'], int):
        missing_fields.append('size')
    if 'version' not in game_details or not isinstance(game_details['version'], int):
        missing_fields.append('version')

    return missing_fields

def update_game_info(game_details, missing_fields):
    """Prompts user to update missing fields in game details."""
    for field in missing_fields:
        new_value = input(f"Enter the {field} (current: {game_details.get(field, 'None')}): ")
        if new_value:
            if field in ['releaseDate', 'size', 'version']:
                game_details[field] = int(new_value)
            else:
                game_details[field] = new_value
    return game_details

def process_games(directory):
    """Processes each JSON file in the given directory to complete missing information."""
    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as json_file:
                game_details = json.load(json_file)

            missing_fields = get_missing_info_fields(game_details)
            if missing_fields:
                print(f"Missing information for {game_details['id']} - {game_details.get('name', 'Unknown')}:")
                print(f"Missing fields: {', '.join(missing_fields)}")
                
                action = input("Do you want to complete the missing information? (y/n): ")
                if action.lower() == 'y':
                    updated_game_details = update_game_info(game_details, missing_fields)
                    with open(file_path, 'w') as json_file:
                        json.dump(updated_game_details, json_file, indent=4)
                    print(f"Updated details for {file_name}")
                else:
                    print(f"Skipped {file_name}")

def main():
    content_types = {
        1: 'base',
        2: 'dlc',
        3: 'update',
        4: 'retro'
    }

    print("Select the type of content you want to process:")
    print("1. Base")
    print("2. DLC")
    print("3. Update")
    print("4. Retro")
    choice = int(input("Enter the number corresponding to your choice: "))

    content_type = content_types.get(choice)
    if not content_type:
        print("Invalid choice. Exiting.")
        return

    if content_type == 'retro':
        retro_path = 'retro'
        subdirectories = [name for name in os.listdir(retro_path) if os.path.isdir(os.path.join(retro_path, name))]
        if not subdirectories:
            print("No subdirectories found in retro. Exiting.")
            return

        print("Select the console:")
        for idx, subdir in enumerate(subdirectories, start=1):
            print(f"{idx}. {subdir}")
        console_choice = int(input("Enter the number corresponding to your choice: "))

        if console_choice < 1 or console_choice > len(subdirectories):
            print("Invalid choice. Exiting.")
            return

        directory = os.path.join(retro_path, subdirectories[console_choice - 1])
    else:
        directory = content_type

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist. Exiting.")
        return

    process_games(directory)

if __name__ == "__main__":
    main()
