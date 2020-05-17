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
    titles = titles[0:50]
    titles = list(map(lambda x: x[0].split(" | ")[0][1:], titles))

    # Run solution for 50 title in all stratified dataset
    for title in titles:
        for data in df[0:1]:

            pairCount, pairScores, pairAverage = formPairs(data)

            # Solution 1
            solution1 = solution_1(title, pairCount, pairAverage)
            t, src1 = parsePair(solution1)

            # Solution 2
            solution2 = solution_2(title, pairScores)
            t, src2 = parsePair(solution2)

            # Solution 3
            solution3 = solution_3(title, pairScores)
            t, src3 = parsePair(solution3)

            # Store solution in CSV file
            src1 = src1.replace(",", " ")
            src2 = src2.replace(",", " ")
            src3 = src3.replace(",", " ")
            row = title + "," + src1 + "," + src2 + "," + src3 + "\n"

            with open("SOLUTION.csv", "a+") as F:
                F.write(row)


"""

# solution method 3
#     same as previous expect that when an average similarity is computed,
#     we make it a weighted average and make the weight of the lower value
#     higher than the higher values

#     the sum of the weights has to be 1. so we divide the weight(1) by the
#     number of occurrences in a geometric progression so that the percent change
#     from the lowest value to the second lowest is the same change as from
#     the second to the third and so on and their sum is 1.

# selected_case = model.predict(newquery, 1)
# print('\n\nselected_case', selected_case)

# query_solution = steps(selected_case)
"""
