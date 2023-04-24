import pygame
import time
from Pyro4 import Proxy, locateNS
from enum import Enum

WIN_TITLE = "Jogo da Velha"
BACKGROUND_COLOR = (224, 216, 150)
LINE_COLOR = (0, 0, 0)
BOX_COLOR = (255, 0, 0)
LINE_WIDTH = 3

FONT_NAME = "comicsans"
FONT_COLOR = (0, 0, 255)

BOARD_WIDTH = 600
BOARD_HEIGHT = 500
BOARD_FONT_SIZE = 110

INFO_WIDTH = 600
INFO_HEIGHT1 = 55
INFO_HEIGHT2 = 55
INFO_PADDING = 5
INFO_FONT_SIZE = 25

def win_height() :
    return BOARD_HEIGHT + INFO_HEIGHT1 + INFO_HEIGHT2

def win_width() :
    return max(BOARD_WIDTH, INFO_WIDTH)

def create_board() :
    # deverá ser substituída pela função ou método adequado do Jogo, para reaver o tabuleiro inicial
    board = ['-'] * 9
    return board

def redraw_window(win: pygame.Surface, board, message_ln1, message_ln2) :
    # desenha fundo
    win.fill(BACKGROUND_COLOR)
    # tamanho das casas do tabuleiro
    square_width = BOARD_WIDTH / 3
    square_height = BOARD_HEIGHT / 3
    # desenha das linhas do tabuleiro
    for i in range(1, 3) :
        # linhas horizontais
        ptw1 = (0, i * square_height)
        ptw2 = (BOARD_WIDTH, i * square_height)
        pygame.draw.line(win, LINE_COLOR, ptw1, ptw2, LINE_WIDTH)
        # linhas verticais
        pth1 = (i * square_width, 0)
        pth2 = (i * square_width, BOARD_HEIGHT)
        pygame.draw.line(win, LINE_COLOR, pth1, pth2, LINE_WIDTH)
    # desenha jogadas
    board_font = pygame.font.SysFont(FONT_NAME, BOARD_FONT_SIZE)
    x_player_text = board_font.render("X", 1, FONT_COLOR)
    o_player_text = board_font.render("O", 1, FONT_COLOR)
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
    info_rect = (INFO_PADDING, BOARD_HEIGHT + INFO_PADDING, INFO_WIDTH - 2*INFO_PADDING, INFO_HEIGHT1 + INFO_HEIGHT2 - 2*INFO_PADDING)
    pygame.draw.rect(win, LINE_COLOR, info_rect, LINE_WIDTH)
    # desenha texto da caixa de informações
    info_font = pygame.font.SysFont(FONT_NAME, INFO_FONT_SIZE)
    info_text = info_font.render(message_ln1, 1, FONT_COLOR)
    pos_txt = (INFO_WIDTH / 2 - info_text.get_width() / 2, BOARD_HEIGHT + INFO_HEIGHT1 / 2 - info_text.get_height() / 2)
    win.blit(info_text, pos_txt)
    info_text = info_font.render(message_ln2, 1, FONT_COLOR)
    pos_txt = (INFO_WIDTH / 2 - info_text.get_width() / 2, BOARD_HEIGHT + INFO_HEIGHT1 + INFO_HEIGHT2 / 2 - info_text.get_height() / 2)
    win.blit(info_text, pos_txt)
    # aplica alterações
    pygame.display.flip()

class InputStatus(Enum) :
    Cancel = 1
    Typing = 2
    Ended = 3

def wait_name_input(user_name) :
    while True :
        for ev in pygame.event.get() :
            if ev.type == pygame.QUIT :
                return InputStatus.Cancel, user_name # usuário cancelou
            elif ev.type == pygame.KEYUP and ev.key == pygame.K_BACKSPACE :
                return InputStatus.Typing, (user_name if user_name.len() > 1 else user_name[:-1]) # remove o ultimo caractere
            elif ev.type == pygame.KEYUP and ev.key == 13 : #código para confirmação [enter]
                return InputStatus.Ended, user_name
            elif ev.type == pygame.KEYUP : # nova letra digitada
                return InputStatus.Typing, user_name + ev.unicode

def wait_mouse_input() :
    while True :
        for ev in pygame.event.get() :
            if ev.type == pygame.QUIT :
                return InputStatus.Cancel, -1 # usuário cancelou
            elif ev.type == pygame.MOUSEBUTTONUP :
                mouse_pos = pygame.mouse.get_pos()
                line = mouse_pos[1] * 3 // BOARD_HEIGHT
                col = mouse_pos[0] * 3 // BOARD_WIDTH
                if line > -1 and line < 3 and col > -1 and col < 3 :
                    return InputStatus.Ended, (line, col) # usuário clicou numa posição válida

def start_player() :
    # trecho 01 inicializando a conexão
    print("Inicializando...")
    ns = locateNS()
    player = Proxy(ns.lookup("Player"))
    game = Proxy(ns.lookup("JogoDaVelha"))
    # trecho 02 inicializando FrontEnd
    pygame.font.init()
    win = pygame.display.set_mode((win_width(), win_height()))
    pygame.display.set_caption(WIN_TITLE)
    board = create_board()
    # trecho 03 nome do usuário
    user_name = ""
    while True :
        redraw_window(win, board, "Digite usuário e tecle enter: ", user_name) # redesenha a janela do game
        status, user_name = wait_name_input(user_name)
        match status :
            case InputStatus.Cancel : # usuário cancelou
                return
            case InputStatus.Ended : # finaliza
                if len(user_name) > 0 : break
    # trecho 04 login
    player.login(user_name)
    game_id = game.match_making(player.get_id())
    game.load_game(game_id)
    player.load_player()
    # trecho 05 aguardando adversário
    message_ln1 = f"Olá, {user_name}! O jogo já vai começar!"
    message_ln2 = "Estamos procurando um adversário!"
    player2 = ""
    while True :
        redraw_window(win, board, message_ln1, message_ln2)
        game.load_game(game_id)
        game_data = game.get_game_data()
        if game_data["player2"]:
            player2 = game_data["player2"]
            break
        else:
            time.sleep(1)
    # trecho 06 inicio do jogo
    while True :
        game.check_win()
        game.load_game(game_id)
        game_data = game.get_game_data()
        
        if game_data["winner"] : break

        if game_data["finished"] : break

        if game_data["current_player"] == player.get_id():
            message_ln2 = f"[{user_name}] vs. [{player2}]"
            message_ln1 = f"É a sua vez! Clique em uma casa e insira um '{player.symbol}'"
            redraw_window(win, game_data["board"], message_ln1, message_ln2)
            status, position = wait_mouse_input()
            match status :
                case InputStatus.Cancel : # usuário cancelou
                    game.exit_game()
                    break
                case InputStatus.Ended : # usuário clicou
                    done = game.do_move(position, player.get_id())
                    if not done :
                        redraw_window(win, game_data["board"], message_ln1, "Posição inválida, tente novamente!")
        else :
            message_ln2 = f"[{user_name}] vs. [{player2}]"
            message_ln1 = "É a vez do seu openente, aguarde um pouco!"
            redraw_window(win, game_data["board"], message_ln1, message_ln2)
            time.sleep(1)

    winner = game_data["winner"]
    message_ln1 = "O jogo terminou!"
    if winner == None :
        message_ln2 = "Foi empate!"
    elif winner == player.get_id() :
        message_ln2 = "Você venceu!"
    else :
        message_ln2 = "Você perdeu!"
    redraw_window(win, game_data["board"], message_ln1, message_ln2)

start_player()