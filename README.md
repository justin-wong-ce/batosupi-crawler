# batosupi-crawler v0.1.1
Image and effect translation crawler + Tabletop Simulator importer for Battle Spirits mod:
https://steamcommunity.com/sharedfiles/filedetails/?id=1629315994

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

TODO: Add effect scraper usage guide

1. Run `main.py`
2. Choose operation. We need to download the images of the cards first, so input `D` or `d`
3. Enter the generation name of the cards you want to import (i.e. BS60, BSC39) and press Enter
    ```
    Battle Spirits card importer v0.1.1
    Download card images from fandom: [D/d]
    Scrape card effects: [S/s]
    Load card names onto cards: [L/l]
    Choice: d
    Please input the card generation abbreviation (i.e. BSC28): CB23
    Continue? [(Y/y)/(N/n)]: 
    ```

4. When cards are done downloading, they are saved in the `./downloads/GENERATION_NAME/assets` folder, open this folder and check for bad images
5. (Continue if you are importing to Tabletop Simulator) Open the deck builder, drag all the downloaded images into it.
6. In the deck builder, export the deck as a `.png` file. If there are more than 69 cards, there will be multiple tabs in the deck builder and you have to export multiple `.png` files and retain the order of the `.png` (**Order: Ascending alphabetical order**)

    ```
    Mode                 LastWriteTime         Length Name
    ----                 -------------         ------ ----
    d-----        2022/07/11      2:38                assets
    -a----        2022/07/11      2:40       58510913 BS60-1.png
    -a----        2022/07/11      2:40           5013 BS60-1.tsdb
    -a----        2022/07/11      2:40       59341844 BS60.png
    -a----        2022/07/11      2:40           5369 BS60.tsdb
    ```

    (BS60.png contains BS02-X08 to BS60-058, BS60-1.png contains BS60-059 to SD56-RV009)
    
7. Open Tabletop Simulator, load save `-` (The one copied earlier), and load an empty table
8. Click on Objects > Components > Cards > Custom Deck and import cards, DO NOT CHANGE THE ORDER OF THE CARDS/SHUFFLE: 
In case of multiple exported images from Deck Builder, have both decks of cards face down, and put first exported image on top of the latter, to retain card order (i.e. BS60 stack on top of BS60-1 stack)
9. Overwrite the save file (Save 0)
10. Rerun `main.py` or continue the script, and input `l`/`L` to load card names

    ```
    Continue? [(Y/y)/(N/n)]: y
    Download card images from fandom: [D/d]
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

11. Enter the card generation name
12. Names will be loaded into "Save -":
13. Cards are now named and imported

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
