from turtle import home
import pygame as pg
from pygame.locals import *

import RootScene
# import TicTacToeScene
from utility import *

RS = RootScene.RootScene
# TS = TicTacToeScene.TicTacToeScene

class ResultScene(RS):
    def __init__(self, screen, result):
        super().__init__()
        self.redraw = True
        self.result_message_rect = None
        self.screen = screen 
        self.result = result
        self.Draw(screen)

    def HandleEvents(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.result_message_rect.collidepoint(mouse_pos):
                    self.ChangeNext(objectFactory('TTT', self.screen, [[None]*3 for _ in range(3)], 1))

    def draw_result(self, screen):
        font = pg.font.Font(None, 50)
        msg = font.render(self.result, 1, (0, 0, 0))
        msg_rect = msg.get_rect(center=(900/2, 600/2))
        self.result_message_rect = pg.Rect(900/2-200, 600/2-150/2, 400,150)
        pg.draw.rect(screen, (0,0,220), self.result_message_rect)
        screen.blit(msg, msg_rect)

    def Draw(self, screen):
        if self.redraw == True:
            self.draw_result(screen)
            self.redraw = False