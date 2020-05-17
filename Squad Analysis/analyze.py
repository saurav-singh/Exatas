import json


def parseData(squadData):
    squadData = squadData["data"]
    titles = []
    qCount = []

    for data in squadData:
        qas = []
        count = 0

        titles.append(data["title"])

        for _data in data["paragraphs"]:
            qas.append(_data["qas"])

        for _data in qas:
            for _ in _data:
                count += 1

        qCount.append(count)
    
    print(len(titles),len(qCount))

    with open("counts.txt", "w+") as f:
        for count in qCount:
            count = str(count) + "\n"
            f.write(count)


if __name__ == "__main__":
    # Read Questions from json
    with open("squadData.json") as data:
        data = json.load(data)

    parseData(data)
