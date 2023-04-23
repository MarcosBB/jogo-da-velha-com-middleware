import pygame

# from JogoDaVelha import JogoDaVelha, Player

WIN_TITLE = "Jogo da Velha"
BACKGROUND_COLOR = (224, 216, 150)
LINE_COLOR = (0, 0, 0)
BOX_COLOR = (255, 0, 0)
LINE_WIDTH = 3

FONT_NAME = "comicsans"
FONT_COLOR = (0, 0, 255)

BOARD_WIDTH = 500
BOARD_HEIGHT = 500
BOARD_FONT_SIZE = 110

INFO_WIDTH = 500
INFO_HEIGHT = 80
INFO_PADDING = 5
INFO_FONT_SIZE = 25

def win_height() :
    return BOARD_HEIGHT + INFO_HEIGHT

def win_width() :
    return max(BOARD_WIDTH, INFO_WIDTH)

def create_board() :
    # deverá ser substituída pela função ou método adequado do Jogo, para reaver o tabuleiro inicial
    board = ['-'] * 9
    return board

def create_player() :
    # deverá ser substituída pelo método adequado de acordo com o Jogo
    return 'X'

def validate_play(user_input, player_char, board) :
    # deverá ser substituída pela função correta de usuário
    # aqui por conveniencia da implementação será atualizado o 'board' e o 'player'
    lin = user_input[0]
    col = user_input[1]
    if user_input == (-1, -1) : #usuário fechou o jogo
        status_ok = False
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

def redraw_window(win: pygame.Surface, board, msg) :
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
    info_rect = (INFO_PADDING, BOARD_HEIGHT + INFO_PADDING, INFO_WIDTH - 2*INFO_PADDING, INFO_HEIGHT - 2*INFO_PADDING)
    pygame.draw.rect(win, LINE_COLOR, info_rect, LINE_WIDTH )
    # desenha texto da caixa de informações
    info_font = pygame.font.SysFont(FONT_NAME, INFO_FONT_SIZE)
    info_text = info_font.render(msg, 1, FONT_COLOR)
    pos_txt = (INFO_WIDTH / 2 - info_text.get_width() / 2, BOARD_HEIGHT + INFO_HEIGHT / 2 - info_text.get_height() / 2)
    win.blit(info_text, pos_txt)
    # aplica alterações
    pygame.display.flip()

def wait_imput() :
    while True :
        for ev in pygame.event.get() :
            if ev.type == pygame.QUIT :
                return (-1, -1) # usuário cancelou
            elif ev.type == pygame.MOUSEBUTTONUP :
                mouse_pos = pygame.mouse.get_pos();
                line = mouse_pos[1] * 3 // BOARD_HEIGHT
                col = mouse_pos[0] * 3 // BOARD_WIDTH
                return (line, col) # usuário clicou

def load_screen(player, game) :
    pygame.font.init()
    win = pygame.display.set_mode((win_width(), win_height()))
    pygame.display.set_caption(WIN_TITLE)
    if game is None :
        board = create_board()
    else :
        board = game.board
    if player is None :
        player_char = create_player()
    else :
        player_char = player.simbolo
        #pegar a informação de qual o simbolo a partidir do jogador
    status_ok = True
    while status_ok :
        # redesenha a janela do game
        redraw_window(win, board, f"Proximo a jogar: {player_char}")
        # espera pela operação do usuário e realiza a validação
        status_ok, player_char, board = validate_play(wait_imput(), player_char, board)

load_screen(None, None)