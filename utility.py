import pygame as pg
from pygame.locals import *

def draw_button(font, text, screen, color, center_pos, left, top, width, height):
    back = font.render(text, 1, (0, 0, 0))
    back_rect = back.get_rect(center=center_pos)
    back_but_rect = pg.Rect(left, top, width,height)
    pg.draw.rect(screen, color, back_but_rect)
    screen.blit(back, back_rect)
    return back_but_rect

def check_horizontal_connection(board, last_move_color, x, y, win_condition, board_size):
    connected_pieces = 1
    piece_to_check = win_condition - 1
    max_index = board_size - 1

    for i in range(min(x, piece_to_check)):
        if board[x-i-1][y] == last_move_color:
            connected_pieces += 1
        else:
            break
    for i in range(min(win_condition-connected_pieces, max_index-x)):
        if board[x+i+1][y] == last_move_color:
            connected_pieces += 1
        else:
            break
    return connected_pieces

def check_vertical_connection(board, last_move_color, x, y, win_condition, board_size):
    connected_pieces = 1
    piece_to_check = win_condition - 1
    max_index = board_size - 1

    for i in range(min(y, piece_to_check)):
        if board[x][y-i-1] == last_move_color:
            connected_pieces += 1
        else:
            break
    for i in range(min(win_condition-connected_pieces, max_index-y)):
        if board[x][y+i+1] == last_move_color:
            connected_pieces += 1
        else:
            break
    return connected_pieces

def check_main_diagnal_connection(board, last_move_color, x, y, win_condition, board_size):
    connected_pieces = 1
    piece_to_check = win_condition - 1
    max_index = board_size - 1

    for i in range(min(x, y, piece_to_check)):
        if board[x-i-1][y-i-1] == last_move_color:
            connected_pieces += 1
        else:
            break
    for i in range(min(win_condition-connected_pieces, max_index-y, max_index-x)):
        if board[x+i+1][y+i+1] == last_move_color:
            connected_pieces += 1
        else:
            break
    return connected_pieces

def check_inverse_diagnal_connection(board, last_move_color, x, y, win_condition, board_size):
    connected_pieces = 1
    piece_to_check = win_condition - 1
    max_index = board_size - 1

    for i in range(min(max_index-x, y, piece_to_check)):
        if board[x+i+1][y-i-1] == last_move_color:
            connected_pieces += 1
        else:
            break
    for i in range(min(win_condition-connected_pieces, max_index-y, x)):
        if board[x-i-1][y+i+1] == last_move_color:
            connected_pieces += 1
        else:
            break
    return connected_pieces

def calculate_block_size(screen_size, offset, blocks):
    return (screen_size - 2 * offset) / blocks