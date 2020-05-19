
'''
Solution Method 0
Description ~
'''
def solution_0(title, pairCount, pairAverage):
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
        solution = "Undetermined"

    return solution


'''
Solution Method 0
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
Description ~ Double highest then average
'''
def solution_3(title, pairScores):
    validPair = []

    for pair in pairScores:
        t, _ = parsePair(pair)
        if title == t:
            scores = sorted(list(pairScores[pair]))

            # Double max score then average
            if len(scores) > 1:
                maxIndex = scores.index(max(scores))
                scores[maxIndex] *= 2
                score = sum(scores) / len(scores)
            else:
                score = scores[0]

            validPair.append((pair, score))

    validPair = sorted(validPair, key=lambda x: x[1], reverse=True)
    solution = validPair[0][0]

    return solution


'''
Solution Method 0
Description ~
'''
def solution_4(title, pairScores):
    validPair = []

    for pair in pairScores:
        t, _ = parsePair(pair)
        if title == t:
            scores = sorted(list(pairScores[pair]))

            # Double max score then average
            if len(scores) > 1:
                minIndex = scores.index(min(scores))
                scores[minIndex] *= 2
                score = sum(scores) / len(scores)
            else:
                score = scores[0]

            validPair.append((pair, score))

    validPair = sorted(validPair, key=lambda x: x[1], reverse=True)
    solution = validPair[0][0]

    return solution


'''
Parse pair into title and solution
'''
def parsePair(pair):
    pair = pair.split(" | ")
    title = pair[0][1:]
    source = pair[1][:-1]
    return title, source
