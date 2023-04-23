from Pyro4 import Proxy, locateNS
import os, time
ns = locateNS()
player = Proxy(ns.lookup("Player"))
game = Proxy(ns.lookup("JogoDaVelha"))

player.login(input("Insira seu username: "))

print(f"Bem vindo ao jogo da velha, {player.get_name()}!")
print("Procurando por um oponente...")

game_id = game.match_making(player.get_id())
game.load_game(game_id)
player.load_player()
print()

while True:
    game.load_game(game_id)
    game_data = game.get_game_data()

    if game_data["player2"]:
        break
    else:
        print("Aguardando um oponente...")
        time.sleep(1)
        os.system("clear")


while True:
    game.check_win()
    game.load_game(game_id)
    game_data = game.get_game_data()

    print(game_data["board"][0] + "|" + game_data["board"][1] + "|" + game_data["board"][2])
    print(game_data["board"][3] + "|" + game_data["board"][4] + "|" + game_data["board"][5])
    print(game_data["board"][6] + "|" + game_data["board"][7] + "|" + game_data["board"][8])

    if game_data["winner"]:
        break

    if game_data["finished"]:
        break

    if game_data["current_player"] == player.get_id():
        print("É a sua vez!")
        position = int(input("Insira a posição que deseja jogar:"))

        done = False
        while not done:
            if position == int(-1):
                game.exit_game()
                break

            done = game.do_move(position, player.get_id())
            if not done:
                print("Posição inválida, tente novamente!")
                position = int(input("Insira a posição que deseja jogar:"))

    else:
        print("Aguarde a vez do seu oponente...")
        time.sleep(1)
        os.system("clear")


os.system("clear")
print(game_data["board"][0] + "|" + game_data["board"][1] + "|" + game_data["board"][2])
print(game_data["board"][3] + "|" + game_data["board"][4] + "|" + game_data["board"][5])
print(game_data["board"][6] + "|" + game_data["board"][7] + "|" + game_data["board"][8])

if game_data["winner"] == player.get_id():
    print("You won!")

if game_data["finished"] and not game_data["winner"]:
    print("Game finished!")

else:
    print("You lost!")

game.exit_game()