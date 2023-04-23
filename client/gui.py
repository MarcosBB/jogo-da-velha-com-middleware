import pygame
import time
from Pyro4 import Proxy, locateNS

CONFIG = {
    'WIN_TITLE': "Jogo da Velha",
    'BACKGROUND_COLOR': (224, 216, 150),
    'LINE_COLOR': (0, 0, 0),
    'BOX_COLOR': (255, 0, 0),
    'LINE_WIDTH': 3,

    'FONT_NAME': "comicsans",
    'FONT_COLOR': (0, 0, 255),

    'BOARD_WIDTH': 600,
    'BOARD_HEIGHT': 500,
    'BOARD_FONT_SIZE': 110,

    'INFO_WIDTH': 600,
    'INFO_HEIGHT1': 55,
    'INFO_HEIGHT2': 55,
    'INFO_PADDING': 5,
    'INFO_FONT_SIZE': 25,
}

this_data = {
    'message_ln1': "conectando..",
    'message_ln2': "conectando..",
    'player': None,
    'game': None,
    'mode': "login"
}

def win_height() :
    return CONFIG['BOARD_HEIGHT'] + CONFIG['INFO_HEIGHT1'] + CONFIG['INFO_HEIGHT2']

def win_width() :
    return max(CONFIG['BOARD_WIDTH'], CONFIG['INFO_WIDTH'])

def create_board() :
    # deverá ser substituída pela função ou método adequado do Jogo, para reaver o tabuleiro inicial
    board = ['-'] * 9
    return board

def create_player() :
    # deverá ser substituída pelo método adequado de acordo com o Jogo
    return 'X'

def validate_input(user_input, player_char, board) :
    # deverá ser substituída pela função correta de usuário
    # aqui por conveniencia da implementação será atualizado o 'board' e o 'player'
    lin = user_input[0]
    col = user_input[1]
    if user_input == (-1, -1) : #usuário fechou o jogo
        status_ok = False
    elif user_input == (5, 5) : #digitando usuário
        status_ok = True
    elif user_input == (6, 6) : #teclou enter com usuário
        status_ok = True
        user = this_data['message_ln2']
        this_data['player'].login(user)
        this_data['message_ln1'] = f"Que bom te ver, {user}!"
        this_data['message_ln2'] = "Procurando por um oponente..."
        this_data['mode'] = 'waiting'
    elif lin > 2 or col > 2 or lin < 0 or col < 0 : # clique inválido
        status_ok = True #jogada inválida mas jogo continua
    else : #clique válido
        square = lin*3 + col
        if board[square] == '-' : #foi clicado numa casa vazia OK
            board[square] = player_char
            player_char = 'O' if player_char == 'X' else 'X'
            status_ok = True
        else : # foi clicado numa casa já usada, jogo continua
            status_ok = True
            # verificar se todas as casas estão cheias para recomeçar
            if board.count('-') == 0 :
                board = create_board()
    return status_ok, player_char, board 

def redraw_window(win: pygame.Surface, board) :
    # desenha fundo
    win.fill(CONFIG['BACKGROUND_COLOR'])
    # tamanho das casas do tabuleiro
    BOARD_WIDTH = CONFIG['BOARD_WIDTH']
    BOARD_HEIGHT = CONFIG['BOARD_HEIGHT']
    square_width = BOARD_WIDTH / 3
    square_height = BOARD_HEIGHT / 3
    # desenha das linhas do tabuleiro
    for i in range(1, 3) :
        # linhas horizontais
        ptw1 = (0, i * square_height)
        ptw2 = (BOARD_WIDTH, i * square_height)
        pygame.draw.line(win, CONFIG['LINE_COLOR'], ptw1, ptw2, CONFIG['LINE_WIDTH'])
        # linhas verticais
        pth1 = (i * square_width, 0)
        pth2 = (i * square_width, CONFIG['BOARD_HEIGHT'])
        pygame.draw.line(win, CONFIG['LINE_COLOR'], pth1, pth2, CONFIG['LINE_WIDTH'])
    # desenha jogadas
    board_font = pygame.font.SysFont(CONFIG['FONT_NAME'], CONFIG['BOARD_FONT_SIZE'])
    x_player_text = board_font.render("X", 1, CONFIG['FONT_COLOR'])
    o_player_text = board_font.render("O", 1, CONFIG['FONT_COLOR'])
    for i in range(0,9) :
        x = i % 3
        y = (i-x)//3
        play = board[i]
        if play == '-': continue
        afast_width = square_width / 2 - (x_player_text.get_width()/2 if play == 'X' else o_player_text.get_width()/2)
        afast_height = square_height / 2 - (x_player_text.get_height()/2 if play == 'X' else o_player_text.get_height()/2)
        pos_txt = (x*square_width + afast_width, y*square_height + afast_height)
        win.blit(x_player_text if play == 'X' else o_player_text, pos_txt)

    # desenha caixa de informações
    INFO_PADDING = CONFIG['INFO_PADDING']
    INFO_WIDTH = CONFIG['INFO_WIDTH']
    INFO_HEIGHT1 = CONFIG['INFO_HEIGHT1']
    INFO_HEIGHT2 = CONFIG['INFO_HEIGHT2']
    info_rect = (INFO_PADDING, BOARD_HEIGHT + INFO_PADDING, INFO_WIDTH - 2*INFO_PADDING, INFO_HEIGHT1 + INFO_HEIGHT2 - 2*INFO_PADDING)
    pygame.draw.rect(win, CONFIG['LINE_COLOR'], info_rect, CONFIG['LINE_WIDTH'])
    # desenha texto da caixa de informações
    info_font = pygame.font.SysFont(CONFIG['FONT_NAME'], CONFIG['INFO_FONT_SIZE'])
    info_text = info_font.render(this_data['message_ln1'], 1, CONFIG['FONT_COLOR'])
    pos_txt = (INFO_WIDTH / 2 - info_text.get_width() / 2, BOARD_HEIGHT + INFO_HEIGHT1 / 2 - info_text.get_height() / 2)
    win.blit(info_text, pos_txt)
    info_text = info_font.render(this_data['message_ln2'], 1, CONFIG['FONT_COLOR'])
    pos_txt = (INFO_WIDTH / 2 - info_text.get_width() / 2, BOARD_HEIGHT + INFO_HEIGHT1 + INFO_HEIGHT2 / 2 - info_text.get_height() / 2)
    win.blit(info_text, pos_txt)
    # aplica alterações
    pygame.display.flip()

def wait_imput() :
    while True :
        for ev in pygame.event.get() :
            if ev.type == pygame.QUIT :
                return (-1, -1) # usuário cancelou
            elif ev.type == pygame.MOUSEBUTTONUP and this_data['mode'] == 'playing' :
                mouse_pos = pygame.mouse.get_pos();
                line = mouse_pos[1] * 3 // CONFIG['BOARD_HEIGHT']
                col = mouse_pos[0] * 3 // CONFIG['BOARD_WIDTH']
                return (line, col) # usuário clicou
            elif ev.type == pygame.KEYUP and this_data['mode'] == 'login' :
                out = 5 #código para digitação de letras
                if ev.key == pygame.K_BACKSPACE :
                    this_data['message_ln2'] = this_data['message_ln2'][:-1]
                elif ev.key == 13 :
                    out = 6 #código para confirmação [enter]
                else :
                    this_data['message_ln2'] += ev.unicode
                return (out, out)

ns = locateNS()
player = Proxy(ns.lookup("Player"))
game = Proxy(ns.lookup("JogoDaVelha"))

this_data['player'] = player
this_data['game'] = game
this_data['message_ln1'] = "Digite usuário e tecle enter: "
this_data['message_ln2'] = ""
this_data['mode'] = "login"
pygame.font.init()
win = pygame.display.set_mode((win_width(), win_height()))
pygame.display.set_caption(CONFIG['WIN_TITLE'])
board = create_board()
player_char = create_player()

status_ok = True
while status_ok :
    # redesenha a janela do game
    redraw_window(win, board)
    # espera pela operação do usuário e realiza a validação
    game_id = None
    status_ok, player_char, board = validate_input(wait_imput(), player_char, board)
    if status_ok and this_data['mode'] == 'waiting' :
        game_id = game.match_making(player.get_id())
        game.load_game(game_id)
        player.load_player()

        while True:
            game.load_game(game_id)
            game_data = game.get_game_data()
            if game_data["player2"]:
                break
            else:
                time.sleep(1)