# NX-DB

NX-DB is a custom database for Nintendo Switch, containing information about games, DLC, updates, and other content.

## Project Structure

The project is organized as follows:

- `base/`: Contains JSON files for base games
- `dlc/`: Contains JSON files for downloadable content (DLC)
- `update/`: Contains JSON files for game updates
- `retro/`: Contains JSON files for retro games
- `forwarder/`: Contains JSON files for forwarders
- `merge.py`: Script to merge all JSON files into a single database
- `newcontent.py`: Script to add or update entries in the database

## Features

### Data Merging (`merge.py`)

The `merge.py` script combines all JSON files from different directories into a single `fulldb.json` file. It traverses the following directories:

- base
- dlc
- update
- forwarder

### Adding and Updating Content (`newcontent.py`)

The `newcontent.py` script allows adding new entries or updating existing entries in the database. It offers the following features:

- Adding new games, DLC, or updates
- Updating existing information
- Storing data in the appropriate directory (base, dlc, update)

## Usage

### Merging Data

To create the `fulldb.json` file containing all data:

```bash
python merge.py
```

### Adding or Updating Content
To add or update entries in the database:
```bash
python newcontent.py
```

Follow the on-screen instructions to enter the required information.

## Data Format
Each entry in the database contains the following fields:

- `id`: Unique identifier of the game/content
- `name`: Name of the game/content
- `description` (optional): Description of the game/content
- `publisher` (optional): Publisher of the game
- `region` (optional): Region of the game
- `releaseDate`: Release date in YYYYMMDD format
- `size` (optional): Size of the game/content in bytes
- `version`: Version of the game/content

## Scripts
#### `merge.py`

This script combines all individual JSON files into a single fulldb.json file. It performs the following actions:

- Traverses the specified directories (base, dlc, update, forwarder)
- Reads each JSON file in these directories
- Combines the data into a single dictionary
- Writes the combined data to fulldb.json

#### `newcontent.py`

This script facilitates the addition and updating of content in the database. It provides the following functionality:

- Allows selection of content type (base, DLC, update)
- Prompts for game ID
- If the game exists, allows updating its information
- If the game doesn't exist, allows entering new game details
- Saves the new or updated information to the appropriate JSON file

## Contributing
Contributions to NX-DB are welcome. Feel free to submit pull requests or open issues to suggest improvements or report bugs.

### How to Contribute
1. Fork the repository
2. Create a new branch for your feature (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## Acknowledgments
- Thanks to all contributors who have helped build and maintain this database
- Nintendo Switch community for their support and input


## Disclaimer
This project is not affiliated with or endorsed by Nintendo. All game names, brands, and registered trademarks belong to their respective owners.