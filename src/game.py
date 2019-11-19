from util import Stack, Queue
from player import Player
import os
import json

dir = os.path.dirname(__file__)
rooms_file = os.path.join(dir, '../rooms.json')

class Game:
    def __init__(self):
      self.load_rooms()
    def load_rooms(self):
      saved_rooms = dict()
      try:
        with open(rooms_file) as json_file:
            saved_rooms = json.load(json_file)
        temp_adj = dict()
        temp_rooms = dict()
        for key, value in saved_rooms['adjacency'].items():
          temp_adj[int(key)] = value
        saved_rooms['adjacency'] = temp_adj
        for key, value in saved_rooms['rooms'].items():
          temp_rooms[int(key)] = value
        saved_rooms['rooms'] = temp_rooms
      except:
        saved_rooms['adjacency'] = dict()
        saved_rooms['rooms'] = dict()
      self.saved_rooms = saved_rooms

    def find_path_to(self, player, target_id):
        starting_room_id = player.current_room.id
        adj = self.saved_rooms['adjacency']
        queue = Queue()
        final_path = None
        visited = set()
        queue.enqueue([starting_room_id])
        while queue.len() > 0:
            path = queue.dequeue()
            vert = path[-1]
            if vert not in visited:
                if vert == target_id:
                   final_path = path
                   break
                visited.add(vert)
                for room in adj[vert].values():
                    new_path = list(path)
                    new_path.append(room)
                    queue.enqueue(new_path)
        if final_path is None:
            return
        new_path = []
        for idx, room in enumerate(final_path):
            if idx > 0:
                lastRoom = final_path[idx - 1]
                for direction in adj[lastRoom]:
                    if adj[lastRoom][direction] == room:
                        new_path.append({'dir': direction, 'next_room': room})
        return new_path


game = Game()
player = Player(game)
player.queue_func(player.init)
player.travel_to_target(55)