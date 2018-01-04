from multiprocessing import Pool
import requests
import json
import itertools
import sys
import random
from collections import Counter


EMAIL = 'joshuabrokaw@gmail.com'
BASE_URL = 'https://mastermind.praetorian.com'

AUTH_TOKEN = {
    'Content-Type': 'application/json',
    'Auth-Token': '2f2bd8f88f8183d7ec98c7df42d9b414a12133f4b0285dfd2d8f4ff5a2776159'
}

TOO_MANY_COMBINATIONS = 100


def resetGame():
    requests.post(BASE_URL + '/reset/',
                  headers=AUTH_TOKEN)


def makeGuess(guess, level):
    print('Making guess... ' + str(guess))

    r = requests.post(BASE_URL + '/level/' + str(level) + '/',
                      data=json.dumps({'guess': guess}),
                      headers=AUTH_TOKEN)

    response = r.json()
    print(response)

    sys.stdout.flush()

    if 'response' in response:
        response = r.json()['response']
        return (response[0], response[1])

    if 'message' in response:
        return True


def evaluate(guess, secret):
    correctWeapons = sum((Counter(secret) & Counter(guess)).values())

    if correctWeapons > 0:
        correctGladiators = sum(c == g for c, g in zip(secret, guess))
    else:
        correctGladiators = 0

    return (correctWeapons, correctGladiators)


def startLevel(level):
    r = requests.get(BASE_URL + '/level/' + str(level) + '/',
                     headers=AUTH_TOKEN)

    response = r.json()

    print('\n\n STARTING LEVEL ' + str(level))
    print(response)

    sys.stdout.flush()

    numGladiators = response['numGladiators']
    numGuesses = response['numGuesses']
    numRounds = response['numRounds']
    numWeapons = response['numWeapons']

    allCombinations = []

   # if str(level) in COMBINATIONS:
    #    allCombinations = COMBINATIONS[str(level)]
    # else:
    allCombinations = list(itertools.permutations(
                           list(range(numWeapons)), numGladiators))

    combinations = allCombinations

    def key(g): return max(Counter(evaluate(g, c)
                                   for c in combinations).values())

    combinationCount = len(combinations)

    print(str(combinationCount) + ' combinations')

    guess = combinations[0]

    while True:
        result = makeGuess(guess, level)

        if result is True:
            break

        combinations = [
            c for c in combinations if evaluate(guess, c) == result]

        combinationCount = len(combinations)

        print(str(combinationCount) + ' combinations')

        if len(combinations) == 1:
            guess = combinations[0]
        else:
            if combinationCount > TOO_MANY_COMBINATIONS:
                guess = combinations[random.randint(0, len(combinations))]
            else:
                guess = min(combinations, key=key)
            print('found min', flush=True)

    return result


def generateAllPermutations(p, r):
    return list(itertools.permutations(list(range(p)), r))


def evaluateParallel(guess):
    initialGuess = [0, 1, 2, 3, 4]

    correctWeapons = sum((Counter(initialGuess) & Counter(guess)).values())

    if correctWeapons > 0:
        correctGladiators = sum(c == g for c, g in zip(initialGuess, guess))
    else:
        correctGladiators = 0

    return (correctWeapons, correctGladiators)


if __name__ == '__main__':
    pool = Pool(5)

    level = 1

    resetGame()

    #COMBINATIONS = {}
    #EVALUATIONS = {}

    #COMBINATIONS = generateAllPermutations(18, 6)

    #combinationLen = len(COMBINATIONS)
    #EVALUATIONS = generateEvaluations(COMBINATIONS)

    #EVALUATIONS = list(pool.map(evaluateParallel, COMBINATIONS))

    #evaluationLen = len(EVALUATIONS)

    while True:
        startLevel(level)
        level += 1


def someshit(secret):
    guess = [0, 1, 2, 3, 4, 5]

    correctWeapons = sum((Counter(secret) & Counter(guess)).values())

    if correctWeapons > 0:
        correctGladiators = sum(c == g for c, g in zip(secret, guess))
    else:
        correctGladiators = 0
