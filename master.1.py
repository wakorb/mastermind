import requests
import json
import itertools
import sys

EMAIL = 'joshuabrokaw@gmail.com'
BASE_URL = 'https://mastermind.praetorian.com'

AUTH_TOKEN = {
    'Content-Type': 'application/json',
    'Auth-Token': '2f2bd8f88f8183d7ec98c7df42d9b414a12133f4b0285dfd2d8f4ff5a2776159'
}


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


def score(self, other):

    correct = len([speg for speg, opeg in zip(self, other) if speg == opeg])

    present = sum([min(self.count(j), other.count(j)) for j in list(range(6))])

    return present, correct


def startLevel(level):
    r = requests.get(BASE_URL + '/level/' + str(level) + '/',
                     headers=AUTH_TOKEN)

    response = r.json()

    print(response)

    numGladiators = response['numGladiators']
    numGuesses = response['numGuesses']
    numRounds = response['numRounds']
    numWeapons = response['numWeapons']

    combinations = list(itertools.permutations(
        list(range(numWeapons)), numGladiators))

    results = [(weapon, gladiator) for weapon in range(numGladiators + 1)
               for gladiator in range(weapon + 1) if not (weapon == numGladiators and gladiator == numGladiators - 1)]

    guess = combinations[0]

    result = makeGuess(guess, level)

    if result is not True:
        S = set(combinations)
        S.difference_update(
            set(p for p in S if score(p, guess) != result))

        while result != (numGladiators, numGladiators):
            if len(S) == 1:
                guess = S.pop()
            else:
                guess = max(combinations, key=lambda x: min(
                    sum(1 for p in S if score(p, x) != res) for res in results))

            result = makeGuess(guess, level)

            if result is not True and result != (numGladiators, numGladiators):
                S.difference_update(
                    set(p for p in S if score(p, guess) != result))
            else:
                break

    return result


resetGame()

startLevel(1)

sys.stdout.flush()

startLevel(2)
