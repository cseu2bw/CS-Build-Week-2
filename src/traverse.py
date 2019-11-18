from player import Player
from room import Room
from util import Stack, Queue
import random

player = Player()
player.init()

traversalPath = []

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
    while q.size() > 0:
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
                    new_path.append(direction)
    return new_path

def travelDirPath(traversal, path):
    for direction in path:
        traversal.append(direction)
        player.travel(direction)

def createTraversalPath(lastDir=None, lastRoom=None, adjacency=dict(), traversal=Stack()):
  global player
  global traversalPath
  if len(adjacency) < 500:
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
        traversal.push(direction)
        traversalPath.append(direction)
        player.travel(direction)
    else:
        path = findShortestPath(adjacency)
        if path is not None:
            dir_path = getDirPath(adjacency, path)
            travelDirPath(traversalPath, dir_path)
            lastDir = dir_path[-1]
            lastRoom = path[-2]
    player.queue_func(createTraversalPath, lastDir, lastRoom)
