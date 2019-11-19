import requests
import sys
import os
import json
import random
from uuid import uuid4
from timeit import default_timer as timer
import random

from actions import Actions
from player import Player

if __name__ == '__main__':
    player = Player()
    miner = Actions(player)
    mining = 0

    # Run forever until interrupted
    while mining < 1:
        # Get the last proof from the server
        miner.get_last_proof()
        new_proof = miner.proof_of_work(
            miner.last_proof.proof, miner.last_proof.difficulty)
        miner.mine(str(new_proof))
        print(miner.message)
        mining += 1