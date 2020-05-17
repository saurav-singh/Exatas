import json


if __name__ == "__main__":
    with open("squadData.json") as F:
        squadData = json.load(F)

    with open("squadTitle.csv") as F:
        titles = F.read()
        titles = titles.split("\n")

    FilterSquad = {
        "version": squadData["version"],
        "data": []
    }

    for item in squadData["data"]:
        if item["title"] in titles:
            FilterSquad["data"].append(item)

    with open("selectedSquad.json", "w+") as F:
        json.dump(FilterSquad, F)
