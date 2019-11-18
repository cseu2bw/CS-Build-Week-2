from player import Player
from room import Room
from util import Stack, Queue
import random
import os

dir = os.path.dirname(__file__)
rooms_file = os.path.join(dir, '../rooms.json')

import json

saved_adjacency = dict()
with open(rooms_file) as json_file:
    saved_adjacency = json.load(json_file)
temp_adj = dict()
for key, value in saved_adjacency.items():
  temp_adj[int(key)] = value
saved_adjacency = temp_adj

player = Player()
player.queue_func(player.init)

def reverseDir(dir):
    if dir == "n":
        return "s"
    if dir == "s":
        return "n"
    if dir == "e":
        return "w"
    if dir == "w":
        return "e"
    else:
        return None

def findShortestPath(adj):
    q = Queue()
    q.enqueue([player.current_room.id])
    visited = set()
    while q.len() > 0:
        path = q.dequeue()
        vert = path[-1]
        if vert not in visited:
            if "?" in adj[vert].values():
                return path
            visited.add(vert)
            for room in adj[vert].values():
                new_path = list(path)
                new_path.append(room)
                q.enqueue(new_path)
    return None

def getDirPath(adj, path):
    new_path = []
    for idx, room in enumerate(path):
        if idx > 0:
            lastRoom = path[idx - 1]
            for direction in adj[lastRoom]:
                if adj[lastRoom][direction] == room:
                    new_path.append({'dir': direction, 'next_room': room})
    return new_path

def travelDirPath(path):
    for dir in path:
        player.travel(dir['dir'], dir['next_room'])

def createTraversalPath(lastDir=None, lastRoom=None, adjacency=saved_adjacency):
  global player
  with open('rooms.json', 'w') as json_file:
    json.dump(adjacency, json_file)
  print("Current room:", player.current_room.id, player.current_room.exits)
  if len(adjacency) < 500:
    print(f"Traversed rooms: {len(adjacency)}")
    if player.current_room.id not in adjacency:
        adj = dict()
        for ext in player.current_room.exits:
            adj[ext] = "?"
        adjacency[player.current_room.id] = adj
    if lastRoom:
        adjacency[lastRoom][lastDir] = player.current_room.id
        adjacency[player.current_room.id][reverseDir(lastDir)] = lastRoom
    lastRoom = player.current_room.id

    cur_adj = adjacency[player.current_room.id]
    unvisited = list()
    for direction, room in cur_adj.items():
        if room == "?":
            unvisited.append(direction)

    if len(unvisited) > 0:
        random.shuffle(unvisited)
        direction = unvisited[0]
        lastDir = direction
        player.travel(direction)
    else:
        path = findShortestPath(adjacency)
        if path is not None:
            dir_path = getDirPath(adjacency, path)
            travelDirPath(dir_path)
            lastDir = dir_path[-1]['dir']
            lastRoom = path[-2]
    player.queue_func(createTraversalPath, lastDir, lastRoom)

createTraversalPath()