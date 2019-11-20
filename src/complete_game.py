from game import Game
from player import Player
import os

name = os.environ['PLAYER_NAME']

game = Game()
player = Player(game)
player.queue_func(player.init)
player.queue_func(player.actions.check_status)
if player.status.name != name:
  player.collect_treasures(10)
  player.sell_items()
  player.change_name(name)
player.go_next_block()