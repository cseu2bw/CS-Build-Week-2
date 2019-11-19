import hashlib
import requests
import os

import sys
import json

# from uuid import uuid4
from timeit import default_timer as timer

import random

node = os.environ['BASE_URL']
token  = os.environ['TOKEN']
token = 'Token ' + token

def proof_of_work(last_proof, difficulty):
    N = difficulty
    start = timer()
    print("Searching for next proof")
    proof = random.random()
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    while valid_proof(last_proof, proof, N) is False:
        proof += 1
    return proof

def valid_proof(last_hash, proof, n):
    guess_hash = hashlib.sha256(f'{last_hash}{proof}'.encode()).hexdigest()
    new_N = '0' * n
    return guess_hash[:6] == new_N

# def get_balance():
#     response = requests.get(url=node + "/bc/last_proof", headers={'Authorization': token})
#     try:
#         data = response.json()
#     except ValueError:
#         print(response)
#     print(data)
#     return data
def init():
    coins_mined = 0
    print("Starting miner")
    # while True:
    r = requests.get(url=node + "/bc/last_proof", headers={'Authorization': token})
    try:
        data = r.json()
        print(data)
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
        return r

    new_proof = proof_of_work(data.get('proof'),data.get('difficulty') )
    post_data = {"proof": new_proof}

    r = requests.post(url=node + "/bc/mine",headers={'Authorization': token}, json=post_data)
    data = r.json()
    if data.get('message') == 'New Block Forged':
        coins_mined += 1
        print("Total coins mined: " + str(coins_mined))
    else:
        print(data.get('message'))


# init()
