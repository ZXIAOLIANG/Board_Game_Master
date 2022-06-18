import pygame as pg
from pygame.locals import *

def draw_button(font, text, screen, color, center_pos, left, top, width, height):
    back = font.render(text, 1, (0, 0, 0))
    back_rect = back.get_rect(center=center_pos)
    back_but_rect = pg.Rect(left, top, width,height)
    pg.draw.rect(screen, color, back_but_rect)
    screen.blit(back, back_rect)
    return back_but_rect
