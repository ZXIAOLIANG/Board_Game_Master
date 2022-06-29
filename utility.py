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

def find_all_lines(coordinate):
    result_set = []
    for pos in range(5):
        lines = find_lines(coordinate, pos)
        result_set.extend(lines)
    return result_set

def find_lines(coordinate, pos_in_line):
    relative_pos = [i - pos_in_line for i in range(5)]

    result_line_set = []

    #horizontal line
    horizontalLine = []
    for rp in relative_pos:
        horizontalLine.append((coordinate[0], coordinate[1] + rp))
    if pos_validator(horizontalLine, 15, 15):
        result_line_set.append(horizontalLine)

    #vertical line
    vertical_line = []
    for rp in relative_pos:
        vertical_line.append((coordinate[0] + rp, coordinate[1]))

    if pos_validator(vertical_line, 15, 15):
        result_line_set.append(vertical_line)

    #diagonal line
    diagonal_line = []
    for rp in relative_pos:
        diagonal_line.append((coordinate[0] + rp, coordinate[1] + rp))
    if pos_validator(diagonal_line, 15, 15):
        result_line_set.append(diagonal_line)

    #reverse diagonal line
    r_diagonal_line = []
    for rp in relative_pos:
        r_diagonal_line.append((coordinate[0] + rp, coordinate[1] - rp))
    if pos_validator(r_diagonal_line, 15, 15):
        result_line_set.append(r_diagonal_line)

    return result_line_set

def pos_validator(pos_line, horizontal_bound, vertical_bound):
    for pos in pos_line:
        if pos[0] < 0 or pos[0] >= horizontal_bound:
            return False
        if pos[1] < 0 or pos[1] >= vertical_bound:
            return False
    return True