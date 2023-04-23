from Pyro4 import Proxy, locateNS
import os, time
ns = locateNS()
player = Proxy(ns.lookup("Player"))

player.login(input("Insira seu username: "))
player_name = player.get_name()

print(f"Bem vindo ao jogo da velha, {player_name}!")
print(f"Procurando por um oponente...")

game = player.find_game()
# while True:
print(game.gameinfo())
    # time.sleep(10)
    # os.system("clear")




