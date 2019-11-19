import requests
import os
import threading
import time
from player import Player
from room import Room
from util import Queue
from status import Status
from timeit import default_timer as timer
import hashlib
import random

base_url = os.environ['BASE_URL']

class Actions:
    def __init__(self, player):
        self.player = player
        self.base_url = base_url
        self.message = ''
        self.status = Status()
        # self.other_player = Status()

    def take(self, item):
        response = requests.post(self.base_url + '/adv/take/',
                                 headers={'Authorization': self.player.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def drop(self, item):
        response = requests.post(self.base_url + '/adv/drop/',
                                 headers={'Authorization': self.player.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def check_price(self, item):
        response = requests.post(self.base_url + '/adv/sell/',
                                 headers={'Authorization': self.player.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def sell(self, item):
        response = requests.post(self.base_url + '/adv/sell/', headers={
                                 'Authorization': self.player.token}, json={'name': item, 'confirm': 'yes'})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def check_status(self):
        response = requests.post(
            self.base_url + '/adv/status/', headers={'Authorization': self.player.token})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.status = Status(data.get('name'), data.get('cooldown'), data.get('encumbrance'), data.get('strength'), data.get('speed'), data.get('gold'), data.get('bodywear'), data.get('footwear'), data.get('inventory'), data.get('status'), data.get('errors'), data.get('messages'))
        print("Response:", data)

    def examine(self, item_or_player):
        response = requests.post(self.base_url + '/adv/examine/', headers={
                                 'Authorization': self.player.token}, json={'name': item_or_player})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        # self.other_player = Status(data.get('name'), data.get('cooldown'), data.get('encumbrance'), data.get('strength'), data.get('speed'), data.get('gold'), data.get('bodywear'), data.get('footwear'), data.get('inventory'), data.get('status'), data.get('errors'), data.get('messages'))
        print("Response:", data)

    def wear(self, item):
        response = requests.post(self.base_url + '/adv/wear/',
                                 headers={'Authorization': self.player.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.status = Status(data.get('name'), data.get('cooldown'), data.get('encumbrance'), data.get('strength'), data.get('speed'), data.get('gold'), data.get('bodywear'), data.get('footwear'), data.get('inventory'), data.get('status'), data.get('errors'), data.get('messages'))
        print("Response:", data)

    def undress(self, item):
        response = requests.post(self.base_url + '/adv/undress/',
                                 headers={'Authorization': self.player.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.status = Status(data.get('name'), data.get('cooldown'), data.get('encumbrance'), data.get('strength'), data.get('speed'), data.get('gold'), data.get('bodywear'), data.get('footwear'), data.get('inventory'), data.get('status'), data.get('errors'), data.get('messages'))
        print("Response:", data)

    def change_name(self, new_name):
        response = requests.post(self.base_url + '/adv/change_name/',
                                 headers={'Authorization': self.player.token}, json={'name': new_name})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.status = Status(data.get('name'), data.get('cooldown'), data.get('encumbrance'), data.get('strength'), data.get('speed'), data.get('gold'), data.get('bodywear'), data.get('footwear'), data.get('inventory'), data.get('status'), data.get('errors'), data.get('messages'))
        print("Response:", data)

    def pray(self):
        response = requests.post(
            self.base_url + '/adv/pray/', headers={'Authorization': self.player.token})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def fly(self, dir):
        if dir not in self.player.current_room.exits:
            print('Invalid direction ' + dir)
            return
        to_send = {'direction': dir}
        response = requests.post(self.base_url + '/adv/fly/', headers={'Authorization': self.player.token}, json=to_send)
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Respose:", data)                        

    def dash(self, dir, num_rooms, next_room_ids):
        if dir not in self.player.current_room.exits:
            print('Invalid direction ' + dir)
            return
        if int(num_rooms) != len(list(next_room_ids)):
            print(f'number of rooms do not match {num_rooms} {next_room_ids}')
            return    
        to_send = {'direction': dir, 'num_rooms': num_rooms, 'next_room_ids': next_room_ids}
        response = requests.post(self.base_url + '/adv/dash/', headers={'Authorization': self.player.token}, json=to_send)
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Respose:", data)

    def carry(self, item):
        response = requests.post(self.base_url + '/adv/carry/',
                                 headers={'Authorization': self.player.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)      

    def receive(self):
        response = requests.post(self.base_url + '/adv/receive/',
                                 headers={'Authorization': self.player.token})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)    

    def get_balance(self):
        response = requests.get(self.base_url + '/bc/get_balance/',
                                 headers={'Authorization': self.player.token})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.message = data.get('messages')[0]
        print("Response:", data)

    def transmogrify(self, item):
        response = requests.post(self.base_url + '/adv/transmogrify/',
                                 headers={'Authorization': self.player.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        self.player.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)



    def proof_of_work(self, last_proof, difficulty):
        N = difficulty
        start = timer()
        print("Searching for next proof")
        proof = random.random()
        print("Proof found: " + str(proof) + " in " + str(timer() - start))
        while self.valid_proof(last_proof, proof, N) is False:
            proof += 1
        return proof       

    def valid_proof(self, last_hash, proof, n):
        guess_hash = hashlib.sha256(f'{last_hash}{proof}'.encode()).hexdigest()
        new_N = '0' * n
        return guess_hash[:6] == new_N 

    def mine_coin(self):
        coins_mined = 0
        print("Starting miner")
        response = requests.get(url=self.base_url + "/bc/last_proof", headers={'Authorization': self.player.token})
        try:
            data = response.json()
            print(data)
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return response
        self.player.next_action_time = time.time() + float(data.get('cooldown'))
        if  len(data.get('messages')) > 1: 
            self.message = data.get('messages')[0]
        new_proof = self.proof_of_work(data.get('proof'),data.get('difficulty') )
        post_data = {"proof": new_proof}

        r = requests.post(url=self.base_url + "/bc/mine",headers={'Authorization': self.player.token}, json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))              
