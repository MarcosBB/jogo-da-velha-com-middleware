import Pyro4
import sqlite3
from jogo_da_velha.JogoDaVelha import JogoDaVelha, Player

# Register the classes with Pyro
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
ns.register("JogoDaVelha", daemon.register(JogoDaVelha))
ns.register("Player", daemon.register(Player))
print()
print("Server is running...")
print()
daemon.requestLoop()