import pygame as pg
from pygame.locals import *
import sys
import time

from scipy.misc import central_diff_weights



board = [[None]*3 for _ in range(3)]
current_player = 1 # player 1 takes first turn, player 2 takes second turn
board_size = 600

pg.init()
fps = 30
cl = pg.time.Clock()
screen = pg.display.set_mode((900, 600), 0, 32)
pg.display.set_caption("Board Game Master")

x_img = pg.image.load('x.png')
o_img = pg.image.load('o.png')

x_img = pg.transform.scale(x_img, (100,100))
o_img = pg.transform.scale(o_img, (100,100))

scene = "menu"

def draw_menu():
    global start_but_rect
    screen.fill((255,255,255)) # white
    font = pg.font.Font(None, 80)
    text = font.render("Board Game Master", 1, (0, 0, 0))
    font.set_italic(True)
    font.set_bold(True)
    # put the title at the center of the screen
    text_rect = text.get_rect(center=(900/2, 200))
    screen.blit(text, text_rect)

    font2 = pg.font.Font(None, 50)
    start_game = font2.render("Start Game", 1, (0, 0, 0))
    start_but_rect = start_game.get_rect(center=(900/2, 300))
    pg.draw.rect(screen, (0,255,0), start_but_rect)
    screen.blit(start_game, start_but_rect)

    pg.display.update()

def draw_game():
    global back_but_rect, pause_but_rect, restart_but_rect, board_rect
    screen.fill((255,255,255))
    pg.draw.line(screen,(0,0,0),(0,0),(0, board_size),7)
    pg.draw.line(screen,(0,0,0),(board_size/3,0),(board_size/3, board_size),7)
    pg.draw.line(screen,(0,0,0),(board_size/3*2,0),(board_size/3*2, board_size),7)
    pg.draw.line(screen,(0,0,0),(board_size,0),(board_size, board_size),7)
    # Drawing horizontal lines
    pg.draw.line(screen,(0,0,0),(0,0),(board_size, 0),7)
    pg.draw.line(screen,(0,0,0),(0,board_size/3),(board_size, board_size/3),7)
    pg.draw.line(screen,(0,0,0),(0,board_size/3*2),(board_size, board_size/3*2),7)
    pg.draw.line(screen,(0,0,0),(0,board_size),(board_size, board_size),7)
    board_rect = pg.Rect(0,0,600,600)

    font = pg.font.Font(None, 50)
    # draw pause button
    pause = font.render("PAUSE", 1, (0, 0, 0))
    pause_rect = pause.get_rect(center=(board_size+150, 150))
    pause_but_rect = pg.Rect(board_size+4, 100, 300,100)
    pg.draw.rect(screen, (255,0,0), pause_but_rect)
    screen.blit(pause, pause_rect)
    # draw back button
    back = font.render("BACK", 1, (0, 0, 0))
    back_rect = back.get_rect(center=(board_size+150, 250))
    back_but_rect = pg.Rect(board_size+4, 200, 300,100)
    pg.draw.rect(screen, (220,220,220), back_but_rect)
    screen.blit(back, back_rect)
    # draw restart button
    restart = font.render("RESTART", 1, (0, 0, 0))
    restart_rect = restart.get_rect(center=(board_size+150, 350))
    restart_but_rect = pg.Rect(board_size+4, 300, 300,100)
    pg.draw.rect(screen, (220,220,0), restart_but_rect)
    screen.blit(restart, restart_rect)

    # display instruction
    screen.fill ((255, 255, 255), (board_size+4, 0, 300,100))
    font2 = pg.font.Font(None, 30)
    instruction = font2.render("Player 1's turn", 1, (0, 0, 0))
    inst_rect = instruction.get_rect(center=(board_size+150, 50))
    screen.blit(instruction, inst_rect)

    pg.display.update()

def draw_pause():
    global pause_message_rect

    font = pg.font.Font(None, 50)
    pause = font.render("Game Paused", 1, (0, 0, 0))
    pause_rect = pause.get_rect(center=(900/2, 600/2))
    pause_message_rect = pg.Rect(900/2-200, 600/2-150/2, 400,150)
    pg.draw.rect(screen, (0,0,220), pause_message_rect)
    screen.blit(pause, pause_rect)

def draw_result(result):
    global result_message_rect

    font = pg.font.Font(None, 50)
    msg = font.render(result, 1, (0, 0, 0))
    msg_rect = msg.get_rect(center=(900/2, 600/2))
    result_message_rect = pg.Rect(900/2-200, 600/2-150/2, 400,150)
    pg.draw.rect(screen, (0,0,220), result_message_rect)
    screen.blit(msg, msg_rect)

def draw_step(mouse_pos):
    global board, current_player, scene

    x, y = mouse_pos
    if x < board_size/3:
        x_index = 0
    elif x < board_size*2/3:
        x_index = 1
    elif x <= board_size:
        x_index = 2

    if y < board_size/3:
        y_index = 0
    elif y < board_size*2/3:
        y_index = 1
    elif y <= board_size:
        y_index = 2
    if board[x_index][y_index] is None:
        if current_player == 1:
            board[x_index][y_index] = True
            screen.blit(x_img,(x_index*200+50, y_index*200+50))
        else:
            board[x_index][y_index] = False
            screen.blit(o_img,(x_index*200+50, y_index*200+50))
        result = check_win()
        if result != "Playing":
            scene = "result"
            draw_result(result)
        else:
            update_instruction()
        pg.display.update()

def draw_previous_steps():
    for x_index in range(3):
        for y_index  in range(3):
            if board[x_index][y_index] == True:
                screen.blit(x_img,(x_index*200+50, y_index*200+50))
            elif board[x_index][y_index] == False:
                screen.blit(o_img,(x_index*200+50, y_index*200+50))
    pg.display.update()

def reset():
    global board, current_player
    current_player = 1
    board = [[None]*3 for _ in range(3)]

def check_win():
    for row in range(3):
        if board[row][0] is not None and board[row][0] == board[row][1] == board[row][2]:
            return "Player " + str(current_player) + " win!"

    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return "Player " + str(current_player) + " win!"

    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return "Player " + str(current_player) + " win!"

    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return "Player " + str(current_player) + " win!"
    # check for draw condition
    draw = True
    for x in range(3):
        for y in range(3):
            if board[x][y] is None:
                draw = False
    if draw:
        return "Draw!"
    return "Playing"

def update_instruction():
    global current_player
    if current_player == 1:
        current_player = 2
    elif current_player == 2:
        current_player = 1

    screen.fill ((255, 255, 255), (board_size+4, 0, 300,100))
    font2 = pg.font.Font(None, 30)
    instruction = font2.render("Player " + str(current_player) + "'s turn", 1, (0, 0, 0))
    inst_rect = instruction.get_rect(center=(board_size+150, 50))
    screen.blit(instruction, inst_rect)

    pg.display.update()


draw_menu()
pg.event.clear()
# run the game loop forever
while True:
    if scene == "menu":
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if start_but_rect.collidepoint(pg.mouse.get_pos()):
                    print("start clicked")
                    scene = "game"
                    draw_game()
    elif scene == "game":
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if back_but_rect.collidepoint(mouse_pos):
                    print("back to menu")
                    scene = "menu"
                    draw_menu()
                elif pause_but_rect.collidepoint(mouse_pos):
                    scene = "pause"
                    draw_pause()
                elif restart_but_rect.collidepoint(mouse_pos):
                    reset()
                    draw_game()
                elif board_rect.collidepoint(mouse_pos):
                    draw_step(mouse_pos)

    elif scene == "pause":
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if pause_message_rect.collidepoint(mouse_pos):
                    scene = "game"
                    draw_game()
                    draw_previous_steps()
    elif scene == "result":
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if result_message_rect.collidepoint(mouse_pos):
                    reset()
                    scene = "game"
                    draw_game()
            
    pg.display.update()
    cl.tick(fps)
