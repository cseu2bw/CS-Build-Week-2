from game import Game
from player import Player
import os
import math

name = os.environ['PLAYER_NAME']

game = Game()
player = Player(game)
if player.status.name != name:
  target_items = int(math.ceil(((1000 - player.status.gold) / 100)))
  if target_items > 0:
    player.collect_treasures(target_items)
    player.sell_items()
  player.change_name(name)
if not player.has_flight:
  player.get_flight()
if not player.has_dash:
  player.get_dash()

while True:
  player.go_next_block()
