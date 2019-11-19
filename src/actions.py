import requests
import os
import threading
import time
from room import Room
from util import Queue

base_url = os.environ['BASE_URL']
token = os.environ['TOKEN']

if token == '' or token is None:
    print('Invalid token')


class Actions:
    def __init__(self):
        self.token = 'Token ' + token
        self.base_url = base_url
        self.next_action_time = time.time()
        self.current_room = Room()
        self.queue = Queue()

    def take(self, item):
        response = requests.post(self.base_url + '/adv/take/',
                                 headers={'Authorization': self.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def drop(self, item):
        response = requests.post(self.base_url + '/adv/drop/',
                                 headers={'Authorization': self.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def check_price(self, item):
        response = requests.post(self.base_url + '/adv/sell/',
                                 headers={'Authorization': self.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def sell(self, item):
        response = requests.post(self.base_url + '/adv/sell/', headers={
                                 'Authorization': self.token}, json={'name': item, 'confirm': 'yes'})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def check_status(self):
        response = requests.post(
            self.base_url + '/adv/status/', headers={'Authorization': self.token})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        # replace with player status
        # self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def examine(self, item_or_player):
        response = requests.post(self.base_url + '/adv/examine/', headers={
                                 'Authorization': self.token}, json={'name': item_or_player})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get(
            'description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def wear(self, item):
        response = requests.post(self.base_url + '/adv/wear/',
                                 headers={'Authorization': self.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        # replace with player status
        # self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def undress(self, item):
        response = requests.post(self.base_url + '/adv/undress/',
                                 headers={'Authorization': self.token}, json={'name': item})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        # replace with player status
        # self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def change_name(self, new_name):
        response = requests.post(self.base_url + '/adv/change_name/',
                                 headers={'Authorization': self.token}, json={'name': new_name})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        # replace with player status
        # self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def pray(self):
        response = requests.post(
            self.base_url + '/adv/pray/', headers={'Authorization': self.token})
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        # replace with player status
        # self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Response:", data)

    def fly(self, dir):
        if dir not in self.current_room.exits:
            print('Invalid direction ' + dir)
            return
        to_send = {'direction': dir}
        response = requests.post(self.base_url + '/adv/fly/', headers={'Authorization': self.token}, json=to_send)
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Respose:", data)                        

    def dash(self, dir, num_rooms, next_room_ids):
        if dir not in self.current_room.exits:
            print('Invalid direction ' + dir)
            return
        if int(num_rooms) != len(list(next_room_ids)):
            print(f'number of rooms do not match {num_rooms} {next_room_ids}')
            return    
        to_send = {'direction': dir, 'num_rooms': num_rooms, 'next_room_ids': next_room_ids}
        response = requests.post(self.base_url + '/adv/dash/', headers={'Authorization': self.token}, json=to_send)
        try:
            data = response.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(response)
            return
        self.next_action_time = time.time() + float(data.get('cooldown'))
        self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
        print("Respose:", data) 