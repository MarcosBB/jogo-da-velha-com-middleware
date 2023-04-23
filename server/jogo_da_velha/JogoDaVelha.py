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
                name TEXT NOT NULL,
                symbol TEXT
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

    def load_player(self, player_id=None):
        id = player_id if player_id else self.id
        self.cursor.execute("SELECT * FROM player WHERE id=?", (id,))
        player_data = self.cursor.fetchone()
        self.id = player_data[0]
        self.name = player_data[1]
        self.symbol = player_data[2]


    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id

    def get_symbol(self):
        return self.symbol
@Pyro4.expose
class JogoDaVelha:
    def __init__(self):
        self.id = None
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

    def load_game(self, game_id=None):
        self.id = game_id if game_id else self.id
        self.cursor.execute("SELECT * FROM game WHERE id=?", (self.id,))
        game_data = self.cursor.fetchone()
        self.player1 = game_data[1]
        self.player2 = game_data[2]
        self.winner = game_data[3]
        self.current_player = game_data[4]
        self.board = json.loads(game_data[5])

    def get_game_data(self):
        return {
            'id': self.id,
            'player1': self.player1,
            'player2': self.player2,
            'board': self.board,
            'current_player': self.current_player,
            'winner': self.winner
        }   

    def create_game(self, player1_id):
        board_str = json.dumps(['-'] * 9)
        self.cursor.execute(
            "INSERT INTO game (player1, board) VALUES (?, ?)", 
            (player1_id, board_str))
        self.database.commit()

        self.cursor.execute("SELECT id FROM game WHERE player1=?", (player1_id,))
        game_data = self.cursor.fetchone()
        return game_data[0]
    
    def join_game(self, player2_id, game_id):
        self.cursor.execute("SELECT id, player1 FROM game WHERE id=?", (game_id,))
        game_data = self.cursor.fetchone()

        current_player = random.choice([game_data[1], player2_id])
        player1_symbol = random.choice(["X", "O"]) 
        player2_symbol = "X" if player1_symbol == "O" else "O"

        self.cursor.execute("UPDATE player SET symbol = ? WHERE id = ?", (player1_symbol, game_data[1]))
        self.cursor.execute("UPDATE player SET symbol = ? WHERE id = ?", (player2_symbol, player2_id))
        self.cursor.execute("UPDATE game SET player2 = ?, current_player = ? WHERE id = ?", (player2_id, current_player, game_id))
        self.database.commit()

        return game_id
    
    def match_making(self, player_id):
        """TODO: Melhorar a lógica de matchmaking
        - retomar partidas inacabadas
        - sair da partida (excluir do banco de dados)
        
        """
        self.cursor.execute("SELECT * FROM game WHERE player2 IS NULL AND player1 != ?", (player_id,))
        
        game_data = self.cursor.fetchone()
        if game_data:
            return self.join_game(player_id, game_data[0])
        else:
            return self.create_game(player_id)

    def check_win(self):
        def set_winner(symbol):
            if self.player1.symbol == symbol:
                winner = self.player1.id
            else:
                winner = self.player2.id
            self.cursor.execute("UPDATE game SET winner = ? WHERE id = ?", (winner, self.id))
            self.database.commit()
            return winner

        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != '-':
                set_winner(self.board[i])
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != '-':
                set_winner(self.board[i])
        if self.board[0] == self.board[4] == self.board[8] != '-':
            set_winner(self.board[0])
        if self.board[2] == self.board[4] == self.board[6] != '-':
            set_winner(self.board[2])
    
    def _swich_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        self.cursor.execute("UPDATE game SET current_player = ? WHERE id = ?", (self.current_player, self.id))
        self.database.commit()

    def do_move(self, position, player_id):
        player = Player()
        player.load_player(player_id)
        if self.board[position] == '-' and self.current_player == player_id:
            
            self.board[position] = player.symbol
            self.cursor.execute("UPDATE game SET board = ? WHERE id = ?", (json.dumps(self.board), self.id))
            self.database.commit()
            self._swich_player()
            return True
        else:
            return False
