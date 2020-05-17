import os
import json
import sqlite3
import numpy as np
import pandas as pd

'''
JSON pair : '(title | source)' 
'''

if __name__ == "__main__":

    ''' CONFIG '''
    saveJson = True
    saveCSV = True

    ''' READ DATA '''

    # Retrieve data from database
    conn = sqlite3.connect("Database.db")
    query = "select c.title, c.source_1, similarity_1 from cases c where c.source_1 in \
            (select source_1 from cases group by source_1 having count(*) > 1)"
    df = pd.read_sql_query(query, conn)
    data = np.array(df)

    # Initialize Pair dictionaries
    pairCount = {}
    pairScores = {}
    pairAverage = {}

    ''' FORM PAIRS '''

    # Form pairCount and pairScore
    for d in data:
        title, src, score = d[0], d[1], float(d[2])
        pair = "(" + title + " | " + src + ")"
        if pair in pairCount:
            pairCount[pair] += 1
            pairScores[pair].append(score)
        else:
            pairCount[pair] = 1
            pairScores[pair] = [score]

    # Form and compute pairAverage
    for pair in pairScores:
        pairAverage[pair] = np.average(pairScores[pair])

    ''' STORE RESULT '''

    # Save Pairs as JSON
    if saveJson:

        if not os.path.exists("JSON"):
            os.mkdir("JSON")

        try:
            os.remove("JSON/pairCount.json")
            os.remove("JSON/pairScore.json")
            os.remove("JSON/pairAverage.json")
        except:
            pass

        with open('JSON/pairCount.json', 'w+') as F:
            json.dump(pairCount, F)

        with open('JSON/pairScore.json', 'w+') as F:
            json.dump(pairScores, F)

        with open('JSON/pairAverage.json', 'w+') as F:
            json.dump(pairAverage, F)

    # Write Pairs to CSV
    if saveCSV:

        if not os.path.exists("CSV"):
            os.mkdir("CSV")

        try:
            os.remove("CSV/PairCount.csv")
            os.remove("CSV/PairScore.csv")
            os.remove("CSV/PairAverage.csv")
        except:
            pass

        with open("CSV/PairCount.csv", "a+") as F:
            for d in pairCount:
                TS = d.split(" | ")
                T = TS[0].replace(",", " ")[1:]
                S = TS[1].replace(",", " ")[:-1]
                row = T + "," + S + "," + str(pairCount[d]) + "\n"
                F.write(row)

        with open("CSV/PairScore.csv", "a+") as F:
            for d in pairScores:
                TS = d.split(" | ")
                T = TS[0].replace(",", " ")[1:]
                S = TS[1].replace(",", " ")[:-1]
                row = T + "," + S + "," + str(pairScores[d]) + "\n"
                F.write(row)

        with open("CSV/PairAverage.csv", "a+") as F:
            for d in pairAverage:
                TS = d.split(" | ")
                T = TS[0].replace(",", " ")[1:]
                S = TS[1].replace(",", " ")[:-1]
                row = T + "," + S + "," + str(pairAverage[d]) + "\n"
                F.write(row)