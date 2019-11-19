import requests
import os
import threading
import time
from room import Room
from util import Queue

base_url = os.environ['BASE_URL']
token  = os.environ['TOKEN']

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
        response = requests.post(self.base_url + '/adv/take/', headers={'Authorization': self.token}, json={'name': item})
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

    def drop(self, item):
        response = requests.post(self.base_url + '/adv/drop/', headers={'Authorization': self.token}, json={'name': item})
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

    def check_price(self, item):
        response = requests.post(self.base_url + '/adv/sell/', headers={'Authorization': self.token}, json={'name': item})
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

    def sell(self, item):
        response = requests.post(self.base_url + '/adv/sell/', headers={'Authorization': self.token}, json={'name': item, 'confirm': 'yes'})
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
