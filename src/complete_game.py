from game import Game
from player import Player
import os
import math

name = os.environ['PLAYER_NAME']

game = Game()
player = Player(game)
player.queue_func(player.init)
player.queue_func(player.actions.check_status)
if player.status.name != name:
  target_items = int(math.ceil(((1000 - player.status.gold) / 100)))
  if target_items > 0:
    player.collect_treasures(target_items)
    player.sell_items()
  player.change_name(name)
player.go_next_block()