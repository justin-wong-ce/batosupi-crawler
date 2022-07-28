# batosupi-crawler v0.0.1
Image crawler + Tabletop Simulator importer for battle spirits

## Pre-requisites
- Python >= 3.2, >= 3.7 is recommended 
- Tabletop Simulator (Only for importing to Tabletop Simulator)
- TS-DeckBuilder.exe, located in `YOUR_TABLETOP_INSTALLATION_FOLDER/Modding/` (Only for importing to Tabletop Simulator)

## Installation
Download/clone the repo

## Usage
### Setup
1. In your `~/Documents/My Games/Tabletop Simulator/Saves` folder, copy an existing save `.json` file and rename it as `TS_Save_0.json`, this will be used later. Skip this if you are only downloading images.

### Usage
1. Run `main.py`
2. Choose operation. We need to download the images of the cards first, so input `D` or `d`
3. Enter the generation name of the cards you want to import (i.e. BS60, BSC39) and press Enter
4. When cards are done downloading, they are saved in the `./downloads/GENERATION_NAME/assets` folder, open this folder
5. (Continue if you are importing to Tabletop Simulator) Open the deck builder, drag all the downloaded images into it.
6. In the deck builder, export the deck as a `.png` file. If there are more than 69 cards, there will be multiple tabs in the deck builder and you have to export multiple `.png` files and retain the order of the `.png`
7. Open Tabletop Simulator, load save `0` (The one copied earlier), and load an empty table
8. Click on Objects > Components > Cards > Custom Deck and import cards, DO NOT CHANGE THE ORDER OF THE CARDS/SHUFFLE: 
In case of multiple exported images from Deck Builder, have both decks of cards face down, and put first exported image on top of the latter, to retain card order
9. Overwrite the save file (Save 0)
10. Rerun `main.py` or continue the script, and input `l`/`L` to load card names
11. Enter the card generation name
12. Names will be loaded into "Save -":
13. Cards are now named and imported
