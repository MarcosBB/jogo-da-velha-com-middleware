from Pyro4 import Proxy, locateNS
import os, time
ns = locateNS()
player = Proxy(ns.lookup("Player"))
game = Proxy(ns.lookup("JogoDaVelha"))

player.login(input("Insira seu username: "))

print(f"Bem vindo ao jogo da velha, {player.get_name()}!")
print(f"Procurando por um oponente...")

game_id = game.match_making(player.get_id())
game.load_game(game_id)
print(game.get_game_data())


