import threading
import requests


# JPG DL FOR BATSPI.com
def bs_img_crawler(names):
    # Download the images and save them based on what page they were on on the server
    test = []
    for entry in names:
        # convert to link
        currLink = "https://batspi.com/card/"
        if entry.find("SD") != -1:
            currLink += "SD" + "/" + entry + ".jpg"
        elif entry.find("BSC") != -1:
            currLink += "BSC" + "/" + entry + ".jpg"
        elif entry.find("PC") != -1:
            currLink += "ETC" + "/" + entry + ".jpg"
        elif entry.find("BS") != -1:
            currLink += "BS" + entry[entry.find("BS") + 2] + "/" + entry + ".jpg"
        else:
            currLink = "ERROR"

        # 2 separate cards for TX cards
        if currLink.find("TX") != -1:
            currLink = currLink[:len(currLink) - 4] + "A" + currLink[len(currLink) - 4:]
            print("DEBUG: " + currLink)
            threading.Thread(target=bs_download_save, args=(currLink, entry + "A")).start()
            test.append(currLink)
            currLink = currLink[:len(currLink) - 5] + "B" + currLink[len(currLink) - 4:]
            print("DEBUG: " + currLink)
            threading.Thread(target=bs_download_save, args=(currLink, entry + "B")).start()
            test.append(currLink)
            continue

        test.append(currLink)
        # spawn a new thread to download the image
        threading.Thread(target=bs_download_save, args=(currLink, entry)).start()


def bs_download_save(image_link, name):
    with open("downloads/" + name + ".jpg", "wb") as f:
        f.write(requests.get(image_link).content)


'''
copy names list from batspi.com, i.e.:
スピリット †
SD58-001 ［スクールバンド］ローリア・シープス (2)
SD58-002 ［スクールバンド］ラビィ・ダーリン「Ba」 (2)
SD58-003 ［スクールバンド］ジャンヌ・ドラニエス「Dr」 (3)
SD58-004 ［スクールバンド］フォンニーナ「Dr」 (3)
SD58-005 ［スクールバンド］グリーフィア・ダルク「Key」 R (2)
SD58-006 ［スクールバンド］ネイ・ランテイル「Ba」 R (2)
SD58-007 ［スクールバンド］ジャコミーナ・キット「Gt」 (2)
SD58-008 ［スクールバンド］リアス・ウロヴォルン「Ba」 R (2)
SD58-009 ［スクールバンド］スピニア・スコール「Vo/Gt」 M (2)
SD58-010 ［スクールバンド］セイクレア・メトゥーム「Vo/Gt」 (2)
SD58-011 ［スクールバンド］リオル・ティーダ「Vo/Gt」 M (2)
SD58-012 ［スクールバンド］モモ・ギュウモンジェ「Gt」 R (2)

ネクサス †
SD58-013 開演！ スクールバンド「Vo/Gt/Key/Ba/Dr」 (2)

マジック †
SD58-014 ピックシュート「Gt」 (2)
SD58-015 スパイラルスティック「Dr」 (2)
BSC23-051 跪いて エブリワン (2)

Xレア †
SD58-X01 ［スクールバンド］レイ・オーバ「Vo/Gt」 X (2)
SD58-X02 ［スクールバンド］ディアナ・フルール「Key」 X (2)
SD58-X03 ［スクールバンド］ノア・フルール「Vo/Gt」 X (2)

差し替えカード †
BS33-079 白晶防壁 (2)
BSC33-RV001 スイートハート (2)
BSC33-CP02 プロデューサーリリ CP (1)

キャンペーンカード †
SD58-CP01 プロデューサーアレックス CP (2)


Then delete empty lines + use below regex search and multi-cursor to add quotes and commas
regex search: "\d "
'''
# TODO: Automate the above step?
names = [
    "BSC31-001",
    "BSC31-002",
    "BSC31-003",
    "BSC31-004",
    "BSC31-005",
    "BSC31-006",
    "BSC31-007",
    "BSC31-008",
    "BSC31-009",
    "BSC31-010",
    "BSC31-011",
    "BSC31-012",
    "BSC31-013",
    "BSC31-014",
    "BSC31-015",
    "BSC31-016",
    "BSC31-017",
    "BSC31-018",
    "BSC31-019",
    "BSC31-020",
    "BSC31-021",
    "BSC31-022",
    "BSC31-023",
    "BSC31-024",
    "BSC31-025",
    "BSC31-026",
    "BSC31-027",
    "BSC31-028",
    "BSC31-029",
    "BSC31-030",
    "BSC31-031",
    "BSC31-032",
    "BSC31-033",
    "BSC31-034",
    "BSC31-035",
    "BSC31-036",
    "BSC31-037",
    "BSC31-038",
    "BSC31-039",
    "BSC31-040",
    "BSC31-041",
    "BSC31-042",
    "BSC31-043",
    "BSC31-044",
    "BSC31-045",
    "BSC31-046",
    "BSC31-047",
    "BSC31-048",
    "BSC31-049",
    "BSC31-050",
    "BSC31-051",
    "BSC31-052",
    "BSC31-053",
    "BSC31-054",
    "BSC31-055",
    "BSC31-056",
    "BSC31-057",
    "BS33-079-4",
    "BSC31-X01",
    "BSC31-X02",
    "BSC31-X03",
    "BSC31-X04",
    "BSC31-X05",
    "BSC31-X06",
    "BSC31-CP01",
    "BSC31-CP02",
    "BSC31-CP03",
    "BSC31-CP04"
]
sortedNames = sorted(names, key=str.lower)
bs_img_crawler(sortedNames)
# Generate dump to stdout to copy to txt, for use with tabletop_name_import.py
# TODO: Auto create the .txt file
for i in range(len(sortedNames)):
    # Find names with 2 "-" and remove the second "-" and the characters after itc
    # Do we actually need to remove it?
    firstDashIndex = sortedNames[i].find("-")
    secondDashIndex = sortedNames[i][firstDashIndex + 1:].find("-")
    if secondDashIndex != -1:
        sortedNames[i] = sortedNames[i][:firstDashIndex + secondDashIndex + 1]
    print(sortedNames[i])
while True:
    if threading.active_count() == 1:
        break
