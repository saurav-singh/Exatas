import pandas as pd
import numpy as np
import sqlite3
import json
from solution import *


def formPairs(data):
    # Initialize Pair dictionary
    pairCount = {}
    pairScores = {}
    pairAverage = {}

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

    return pairCount, pairScores, pairAverage


if __name__ == "__main__":

    # Retrieve data
    conn = sqlite3.connect("Database.db")
    query = "select c.title, c.source_1, c.similarity_1 from cases c where c.source_1 in \
            (select source_1 from cases group by source_1 having count(*) > 1)"
    df = pd.read_sql_query(query, conn)
    data = np.array(df)

    # Form Global pairs
    PAIRCOUNT, PAIRAVERAGAE, PAIRSCORES = formPairs(data)

    # Stratify shuffeled data in 12 subsets
    np.random.seed(0)
    np.random.shuffle(data)
    size = len(data)
    N = int(np.ceil(size / 12))
    stop = 0
    df = []

    for _ in range(12):
        stop = size if stop > size else stop + N
        df.append(data[0:stop])

    # Retrieve top 50 titles
    titles = sorted(PAIRCOUNT.items(), key=lambda x: x[1], reverse=True)
    titles = list(map(lambda x: x[0].split(" | ")[0][1:], titles))
    titles = list(dict.fromkeys(titles))
    titles = titles[0:50]

    # Run solution for 50 title in all stratified dataset
    for title in titles:
        for data in df:

            pairCount, pairScores, pairAverage = formPairs(data)

            # Solution 0
            solution0 = solution_0(title, pairCount, pairAverage)
            try:
                t, src0 = parsePair(solution0)
            except:
                src0 = solution0

            # Solution 1
            solution1 = solution_1(title, pairCount, pairAverage)
            t, src1 = parsePair(solution1)

            # Solution 2
            solution2 = solution_2(title, pairScores)
            t, src2 = parsePair(solution2)

            # Solution 3
            solution3 = solution_3(title, pairScores)
            t, src3 = parsePair(solution3)

            solution4 = solution_4(title, pairScores)
            t, src4 = parsePair(solution4)

            # Store solution in CSV file
            src0 = src0.replace(",", " ")
            src1 = src1.replace(",", " ")
            src2 = src2.replace(",", " ")
            src3 = src3.replace(",", " ")
            src4 = src4.replace(",", " ")
            row = title + "," + src0 + "," + src1 + "," + \
                src2 + "," + src3 + "," + src4 + "\n"

            # Write to csv file
            csvFile = "SOLUTION/0-" + str(len(data)) + ".csv"
            with open(csvFile, "a+") as F:
                F.write(row)
