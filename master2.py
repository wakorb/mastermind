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


def startLevel(level):
    r = requests.get(BASE_URL + '/level/' + str(level) + '/',
                     headers=AUTH_TOKEN)

    response = r.json()

    print('\n\n STARTING LEVEL ' + str(level))
    print(response)
    sys.stdout.flush()

    return response


def makeGuess(guess, level):
    print('Making guess... ' + str(guess))

    r = requests.post(BASE_URL + '/level/' + str(level) + '/',
                      data=json.dumps({'guess': guess}),
                      headers=AUTH_TOKEN)

    response = r.json()

    print(response)
    sys.stdout.flush()

    return response


def evaluate(guess, secret):
    correctWeapons = sum((Counter(secret) & Counter(guess)).values())

    if correctWeapons > 0:
        correctGladiators = sum(c == g for c, g in zip(secret, guess))
    else:
        correctGladiators = 0

    return (correctWeapons, correctGladiators)


def quack(level):

    combinations = allCombinations

    combinationCount = len(combinations)

    print(str(combinationCount) + ' combinations')

    guess = combinations[0]

    while True:

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


def someshit():
    numWeapons = 22
    numGladiators = 6

    guesses = []

    counter = 0
    lower = 0

    while counter < numWeapons:
        upper = lower + numGladiators

        if upper > numWeapons:
            guess = list(range(numWeapons - numGladiators, numWeapons))
        else:
            guess = list(range(lower, upper))

        guesses.append(guess)

        lower = upper
        counter += numGladiators

    test = 0
    test += 1


def playGame():

    pool = Pool(processes=4)

    level = 1
    S = []
    guess = []

    def maxFunc(guess): return max(Counter(evaluate(guess, s)
                                           for s in S).values())

    def minimax(guess): return min(S, key=maxFunc)

    roundState = startLevel(level)

    while True:

        if 'response' in roundState:
            # do something
            test = 0

        if 'message' in roundState:
            level += 1
            roundState = startLevel(level)
            continue

        if 'error' in roundState:
            print(roundState)
            break

        numGladiators = roundState['numGladiators']
        numGuesses = roundState['numGuesses']
        numRounds = roundState['numRounds']
        numWeapons = roundState['numWeapons']

        S = list(itertools.permutations(
            list(range(numWeapons)), numGladiators))

        roundState = makeGuess(guess, level)


if __name__ == '__main__':

    resetGame()

    playGame()
