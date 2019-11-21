from game import Game
from player import Player
import os
import math

try:
  name = os.environ['PLAYER_NAME']
except:
  print("Please set desired name in .env file (variable 'PLAYER_NAME')")

game = Game()
player = Player(game)
player.queue_func(player.init)

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

# player.queue_func(player.actions.warp)
# player.init()
# player.travel_to_target(383)
# player.queue_func(player.actions.undress, 'well-crafted boots')
# player.queue_func(player.actions.drop, 'well-crafted boots')
# player.travel_to_target(495)
# player.queue_func(player.actions.take, 'well-crafted boots')
# player.queue_func(player.actions.wear, 'well-crafted boots')
while True:
  player.mine_next_block()
