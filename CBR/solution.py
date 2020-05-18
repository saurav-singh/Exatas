
'''
Solution Method 1
Description ~
'''


def solution_1(title, pairCount, pairAverage):
    validPair = []
    solution = []

    # Retrieve all valid pairs which are pairs containing given title
    for pair in pairCount:
        t, _ = parsePair(pair)
        if title == t:
            validPair.append((pair, pairCount[pair]))

    # Find the solution(s) - pair with highest count
    validPair = sorted(validPair, key=lambda x: x[1], reverse=True)
    solution.append(validPair.pop(0))

    # Find more solutions if it exists (more than one source with highest count)
    for pair in validPair:
        if pair[1] == solution[0][1]:
            solution.append(pair)
        else:
            break

    # Final solution is the pair if it is the higest count
    if len(solution) == 1:
        solution = solution[0][0]

    # For multiple solution, final solution has higher average similarity score
    else:
        scores = list(map(lambda x: pairAverage[x[0]], solution))
        index = scores.index(max(scores))
        solution = solution[index][0]

    return solution


'''
Solution Method 2
Description ~
'''


def solution_2(title, pairScores):
    validPair = []

    for pair in pairScores:
        t, _ = parsePair(pair)
        if title == t:
            score = max(list(pairScores[pair]))
            validPair.append((pair, score))

    validPair = sorted(validPair, key=lambda x: x[1], reverse=True)
    solution = validPair[0][0]

    return solution


'''
Solution Method 3
Description ~
'''


def solution_3(title, pairScores):
    validPair = []

    for pair in pairScores:
        t, _ = parsePair(pair)
        if title == t:
            scores = sorted(list(pairScores[pair]))

            # Compute weights
            # weights = list(map(lambda x: 1-x, scores))
            # _sum = sum(weights)
            # weights = list(map(lambda x: round(x/_sum, 5), weights))

            # Comupute weighted average
            # for i in range(len(scores)):
            #     scores[i] = scores[i] * weights[i]

            score = sum(scores) / len(scores)
            
            validPair.append((pair, score))

    validPair = sorted(validPair, key=lambda x: x[1], reverse=True)
    solution = validPair[0][0]

    return solution


def parsePair(pair):
    pair = pair.split(" | ")
    title = pair[0][1:]
    source = pair[1][:-1]
    return title, source

"""
# solution method 3
#     same as previous expect that when an average similarity is computed,
#     we make it a weighted average and make the weight of the lower value
#     higher than the higher values

#     the sum of the weights has to be 1. so we divide the weight(1) by the
#     number of occurrences in a geometric progression so that the percent change
#     from the lowest value to the second lowest is the same change as from
#     the second to the third and so on and their sum is 1.
"""