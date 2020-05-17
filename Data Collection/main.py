from code import *


'''
Add one line of record to csv file (temp)
'''


# def AddtoFile(fileName, rowData):
#     try:
#         row = rowData["index"] + "," + \
#             rowData["id"] + "," + \
#             rowData["question"] + "," + \
#             rowData["answer"] + "," + \
#             rowData["preprocessQ"]

#         for val in rowData["values"]:
#             # Remove   undefined ascii charater
#             # Replace all commas with <.> for writing in csv
#             val = val.encode(encoding='ascii', errors='replace').decode()
#             val = val.replace(",", "<.>")
#             row += "," + val

#         row += "\n"

#         with open(fileName, "a+", encoding="utf-8") as F:
#             F.write(row)

#     except:
#         return


'''
Main Function
'''

if __name__ == "__main__":

    N = retrieveRowCount()
    cnt = 0

    for i in range(N):
        d = retrieveRow(i)
        if (len(d["answer"]) == 0):
            cnt += 1

    print(cnt)

    # start = 0

    # stop = 100

    # fileName = str(start) + "-" + str(stop) + ".csv"

    # for i in range(start, stop):

    #     print("Current index", i, "/", stop)

    #     # Retrieve i-th row from DB
    #     data = retrieveRow(i)

    #     # Preprocess Question
    #     q = filterStopwords(data["question"])
    #     q = q.replace("?", "").rstrip()

    #     # API Call
    #     response = apiCall(q)

    #     # No data returned from the API
    #     if len(response) == 0:
    #         continue

    #     # Apply BERT | Cos Similarity for ranking
    #     try:
    #         for res in response:
    #             sentence1 = data["question"]
    #             sentence2 = res["title"] + " " + res["abstract"]
    #             res["score"] = bert(sentence1, sentence2)
    #     except:
    #         continue

    #     # Rank and store result to database as outcome
    #     ranked = sorted(response, key=lambda res: res["score"], reverse=True)

    #     values = [""] * 25
    #     index = 0

    #     for r in ranked:
    #         values[index] = r["title"].replace("'", "")
    #         values[index+1] = r["abstract"].replace("'", "")
    #         values[index+2] = r["author"].replace("'", "")
    #         values[index+3] = r["source"].replace("'", "")
    #         values[index+4] = r["sourceURL"].replace("'", "")
    #         index += 5

    #     # updateRow(i, values)

    #     # Add data to file
    #     rowData = {
    #         "index": str(i),
    #         "id": data["ID"],
    #         "question": data["question"],
    #         "answer": data["answer"],
    #         "preprocessQ": q,
    #         "values": values
    #     }

    #     AddtoFile(fileName, rowData)
