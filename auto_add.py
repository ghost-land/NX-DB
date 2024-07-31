import asyncio
import json
import os
from datetime import datetime, date
import rawg

# RAWG API configuration
api_key = ''

def reformat_date(date_str):
    """Reformats a date from the YYYY-MM-DD format to YYYYMMDD and returns it as an integer."""
    if isinstance(date_str, str):
        try:
            # Parse the date in YYYY-MM-DD format
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            # Reformat the date to YYYYMMDD
            reformatted_date = int(date_obj.strftime('%Y%m%d'))
            return reformatted_date
        except ValueError:
            return None  # Default value in case of formatting error
    else:
        return None  # Default value if it's not a string

async def fetch_game_info(name):
    """Fetches game information from the RAWG API."""
    async with rawg.ApiClient(rawg.Configuration(api_key={'key': api_key})) as api_client:
        api = rawg.GamesApi(api_client)
        try:
            response = await api.games_list(search=name, search_precise=True)
            if response.results:
                return response.results[0]
            else:
                print(f"[INFO] No results found for the game '{name}'")
                return None
        except Exception as e:
            print(f"Exception when calling GamesApi->games_list: {e}")
            return None

async def process_games(directory):
    """Processes each JSON file in the given directory to complete missing information."""
    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as json_file:
                game_details = json.load(json_file)
                print(f"Processing file: {file_name}")

            name = game_details.get('name')
            if name:
                base_name = name.split('[')[0].strip()
                game_info = await fetch_game_info(base_name)
                if game_info:
                    release_date = game_info.released

                    # Convert the date to a string if necessary
                    if isinstance(release_date, date):
                        release_date = release_date.strftime('%Y-%m-%d')
                    
                    print(f"String before formatting: {release_date}")  # Debugging
                    formatted_date = reformat_date(release_date)
                    print(f"String after formatting: {formatted_date}")

                    # Assign the formatted string directly if it's not None
                    if formatted_date is not None:
                        game_details['releaseDate'] = formatted_date
                    
                print('——————————————————————————————————————————————')
                print(f"        Name | {game_info.name}")
                print(f"    Released | {game_info.released or 'Not available'}")
                print(f"      Rating | {game_info.rating or 'Not available'}")
                print(f"    Website | {getattr(game_info, 'website', 'Not available') or 'Not available'}")
                print(f"  Metacritic | {getattr(game_info, 'metacritic', 'Not available') or 'Not available'}")
                print(f"Formatted String | {game_details.get('releaseDate', 'Not available')}")
                print('——————————————————————————————————————————————')
                print()

                # Write the data back to the JSON file
                with open(file_path, 'w') as json_file:
                    json.dump(game_details, json_file, indent=4, separators=(',', ': '))
            else:
                print(f"No information found for the game '{base_name}'")

async def main():
    content_types = {1: 'base', 2: 'dlc', 3: 'update', 4: 'retro'}

    print("Select the type of content you want to process:")
    print("1. Base\n2. DLC\n3. Update\n4. Retro")
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
        print(f"The directory {directory} does not exist. Exiting.")
        return

    print(f"Processing games in directory: {directory}")
    await process_games(directory)

if __name__ == "__main__":
    asyncio.run(main())
