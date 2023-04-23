import sqlite3
import Pyro4
import random
import json
    
@Pyro4.expose
class Player:
    def __init__(self):
        self.id = None
        self.name = None
        self.symbol = None
        self.database = sqlite3.connect('database.db')
        self.cursor = self.database.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        self.database.commit()        

    def login(self, name):
        self.cursor.execute("SELECT * FROM player WHERE name=?", (name,))
        player_data = self.cursor.fetchone()
        if player_data:
            self.name = player_data[1]
            self.id = player_data[0]
        else:
            self.cursor.execute("INSERT INTO player (name) VALUES (?)", (name,))
            self.cursor.execute("SELECT id FROM player WHERE name=?", (name,))
            player_data = self.cursor.fetchone()
            self.id = player_data[0]
            self.name = name

        self.database.commit()

    def find_game(self):
        game = JogoDaVelha()
        game.match_making(self)
        return game

    def get_name(self):
        return self.name

@Pyro4.expose
class JogoDaVelha:
    def __init__(self):
        self.board = None
        self.player1 = None
        self.player2 = None
        self.current_player = None

        self.database = sqlite3.connect('database.db')
        self.cursor = self.database.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player1 INTEGER REFERENCES player(id) NOT NULL,
            player2 INTEGER REFERENCES player(id),
            winner INTEGER REFERENCES player(id),
            current_player INTEGER REFERENCES player(id),
            board ARRAY NOT NULL
        )''')
        self.database.commit()

    def create_game(self, player1):
        self.player1 = player1
        self.board = ['-'] * 9
        board_str = json.dumps(self.board)
        self.cursor.execute(
            "INSERT INTO game (player1, board) VALUES (?, ?)", 
            (self.player1.id, board_str))
        self.database.commit()
        print("Jogo criado")

    def join_game(self, player2, game_id):
        self.cursor.execute("UPDATE game SET player2 = ? WHERE id = ?", (player2.id, game_id))
        
        self.cursor.execute("SELECT * FROM game WHERE id=?", (game_id,))
        game_data = self.cursor.fetchone()
        
        self.player1 = game_data[1]
        self.player2 = player2
        self.board = game_data[4]
        self.current_player = game_data[5]
        self.database.commit()
    
    def match_making(self, player):
        self.cursor.execute("SELECT * FROM game WHERE player2 IS NULL AND player1 != ?", (player.id,))

        game_data = self.cursor.fetchone()
        if game_data:
            self.join_game(player, game_data[0])
        else:
            self.create_game(player)
        return self

