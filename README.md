# batosupi-crawler v0.0.2
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
3. Enter the generation name of the cards you want to import (i.e. BS60, BSC39) and press Enter![image](https://user-images.githubusercontent.com/51811017/181442906-9dc175cb-5b5c-425a-a8e1-5968561943c7.png)

4. When cards are done downloading, they are saved in the `./downloads/GENERATION_NAME/assets` folder, open this folder
5. (Continue if you are importing to Tabletop Simulator) Open the deck builder, drag all the downloaded images into it.
6. In the deck builder, export the deck as a `.png` file. If there are more than 69 cards, there will be multiple tabs in the deck builder and you have to export multiple `.png` files and retain the order of the `.png`![image](https://user-images.githubusercontent.com/51811017/181443135-7e97c74a-7a57-4614-9322-b56b879a8d12.png)

    (BS60.png contains BS02-X08 to BS60-058, BS60-1.png contains BS60-059 to SD56-RV009)

7. Open Tabletop Simulator, load save `0` (The one copied earlier), and load an empty table
8. Click on Objects > Components > Cards > Custom Deck and import cards, DO NOT CHANGE THE ORDER OF THE CARDS/SHUFFLE: 
In case of multiple exported images from Deck Builder, have both decks of cards face down, and put first exported image on top of the latter, to retain card order (i.e. BS60 stack on top of BS60-1 stack)
9. Overwrite the save file (Save 0)
10. Rerun `main.py` or continue the script, and input `l`/`L` to load card names
![image](https://user-images.githubusercontent.com/51811017/181443908-77deaec5-8367-4a07-affd-d5161368c3b2.png)

11. Enter the card generation name
12. Names will be loaded into "Save -":
13. Cards are now named and imported

## Troublshooting
- `AssertionError` with files_lines != cards:  ![image](https://user-images.githubusercontent.com/51811017/181444362-44f49a86-e766-41c1-af00-806005372ec0.png)

    Check the txt file generated in the `./decks` directory, see if there are any missing or duplicate card names. Remember to retain alphabetical order.
