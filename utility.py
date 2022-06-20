import pygame as pg
from pygame.locals import *
from MenuScene import MenuScene

from TicTacToeScene import *
from ResultScene import *
from SelectGameScene import *
from PauseScene import *

def draw_button(font, text, screen, color, center_pos, left, top, width, height):
    back = font.render(text, 1, (0, 0, 0))
    back_rect = back.get_rect(center=center_pos)
    back_but_rect = pg.Rect(left, top, width,height)
    pg.draw.rect(screen, color, back_but_rect)
    screen.blit(back, back_rect)
    return back_but_rect

def objectFactory(className, *args):
    arguments = list(args)
    if className == 'TTT':
        screen, board, player = arguments
        return TicTacToeScene(screen, board, player)
    elif className == 'Menu':
        screen = arguments[0]
        return MenuScene(screen)
    elif className == 'Result':
        screen, result = arguments
        return ResultScene(screen, result)
    elif className == 'SelectGame':
        screen = arguments[0]
        return SelectGameScene(screen)
    elif className == 'Pause':
        screen, board, player = arguments
        return PauseScene(screen, board, player)
