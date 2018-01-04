import requests
import json
import random
import itertools
import collections

EMAIL = 'joshuabrokaw@gmail.com'
BASE_URL = 'https://mastermind.praetorian.com'

AUTH_TOKEN = {
    'Content-Type': 'application/json',
    'Auth-Token': '2f2bd8f88f8183d7ec98c7df42d9b414a12133f4b0285dfd2d8f4ff5a2776159'
}


def resetGame():
    requests.post(BASE_URL + '/reset/',
                  headers=AUTH_TOKEN)


def makeGuess(guess):
    r = requests.post(BASE_URL + '/level/1/',
                      data=json.dumps({'guess': guess}),
                      headers=AUTH_TOKEN)

    response = r.json()['response']

    print('Making guess... ' + str(guess) + ' => ' + str(response))

    return response


# def reduceCombinations():


# if (response[1] == numGladiator)
# you win the round
