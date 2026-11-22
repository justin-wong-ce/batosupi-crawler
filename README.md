# batosupi-crawler v0.3.0
Image and effect translation crawler + Tabletop Simulator importer for Battle Spirits mod:
https://steamcommunity.com/sharedfiles/filedetails/?id=1629315994

## Pre-requisites
- Python >= `3.7` is recommended 
- Tabletop Simulator (Only for importing to Tabletop Simulator)
- TS-DeckBuilder.exe, located in `YOUR_TABLETOP_INSTALLATION_FOLDER/Modding/` (Only for importing to Tabletop Simulator)

## Installation
Download/clone the repo

## Usage
### Setup
1. In your `~/Documents/My Games/Tabletop Simulator/Saves` folder, copy an existing save `.json` file and rename it as `TS_Save_-.json`, this will be used later. Skip this if you are only downloading images.

### Usage - Downloading Images

1. Use a Chromium-based browser (Chrome, Edge, etc.) to open the [Bandai TCG Plus](https://www.bandai-tcg-plus.com/card?card_set[]=1053&game_title_id=7&limit=120&offset=0&reverse_card=0) site to extract HAR data
   1. Select the card pack, i.e. `CB23`
   2. Open developer tools (F12), then select the network tab
   3. Reload the page, scroll up and down and ensure all images are loaded
      4. If there are flip cards, click on the flip icon to ensure both sides are loaded
      5. Proceed to other numbered pages at the bottom if more cards are there
   6. Right click, and select `Copy -> Copy all as HARD (sanitized)`
   7. Paste into har.json
2. Run `main.py`
3. Choose operation. We need to download the images of the cards first, so input `H` or `h`
4. Enter the generation name of the cards you want to import (i.e. `BS60`, `BSC39`) and press Enter
    ```
    Battle Spirits card importer v0.3.0
    Download card images (fandom/batspi): [D/d]
    Download card images (HAR): [H/h]
    Scrape card effects: [S/s]
    Load card names onto cards: [L/l]
    Choice: h
    Please input the card generation abbreviation (i.e. BSC28): CB23
    Processing set 'CB23'...
    ...
    Done processing set CB23
    Continue? [(Y/y)/(N/n)]: 
    ```

5. When cards are done downloading, they are saved in the `./downloads/GENERATION_NAME/assets` folder, open this folder and check for bad images
6. (Continue if you are importing to Tabletop Simulator) Open the deck builder, drag all the downloaded images into it.
7. In the deck builder, export the deck as a `.png` file. If there are more than 69 cards, there will be multiple tabs in the deck builder and you have to export multiple `.png` files and retain the order of the `.png` (**Order: Ascending alphabetical order**)

    ```
    Mode                 LastWriteTime         Length Name
    ----                 -------------         ------ ----
    d-----        2022/07/11      2:38                assets
    -a----        2022/07/11      2:40       58510913 BS60-1.png
    -a----        2022/07/11      2:40       59341844 BS60.png
    ```

    (`BS60.png` contains `BS02-X08` to `BS60-058`, `BS60-1.png` contains `BS60-059` to `SD56-RV009`)
    
8. Open Tabletop Simulator, load save `-` (The one copied earlier), and load an empty table
9. Click on Objects > Components > Cards > Custom Deck and import cards, DO NOT CHANGE THE ORDER OF THE CARDS/SHUFFLE: 
In case of multiple exported images from Deck Builder, have both decks of cards face down, and put first exported image on top of the latter, to retain card order (i.e. `BS60` stack on top of `BS60-1` stack)
10. Overwrite the save file (Save 0)
11. Rerun `main.py` or continue the script, and input `l`/`L` to load card names

    ```
    Continue? [(Y/y)/(N/n)]: y
    Download card images (fandom/batspi): [D/d]
    Download card images (HAR): [H/h]
    Scrape card effects: [S/s]
    Load card names onto cards: [L/l]
    Choice: l
    Please input the card generation abbreviation (i.e. BSC28): CB23
    ...
    CB23-001
    CB23-002
    CB23-003
    ...
    file_lines: 69, cards: 69
    Imported
    Continue? [(Y/y)/(N/n)]:
    ```
12. Enter the card generation name
13. Names will be loaded into `TS_Save_-.json`
14. Cards are now named and imported, save the cards as a Collection in Tabletop Simulator


### Usage - Download effects
(TODO)

## Troublshooting
- `AssertionError` with files_lines != cards:
    ```
    file_lines: 70, cards: 69
    Traceback (most recent call last):
      File "G:\CRAWLER\batosupi-crawler\main.py", line 13, in <module>
        tabletop_name_import.tabletopNameImport(cardGenerationName)
      File "G:\CRAWLER\batosupi-crawler\tabletop_name_import.py", line 44, in tabletopNameImport
        assert len(cards) == len(file_lines)
    AssertionError
    ```
    
    Check the txt file generated in the `./decks` directory, see if there are any missing or duplicate card names. Remember to retain alphabetical order.
