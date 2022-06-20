from turtle import home
import pygame as pg
from pygame.locals import *

import RootScene
# import TicTacToeScene
from utility import *

RS = RootScene.RootScene
# TS = TicTacToeScene.TicTacToeScene

class PauseScene(RS):
    def __init__(self, screen, board, current_player):
        super().__init__()
        self.redraw = True
        self.pause_message_rect = None
        self.screen = screen 
        self.board = board
        self.current_player = current_player
        self.Draw(screen)

    def HandleEvents(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.pause_message_rect.collidepoint(mouse_pos):
                    self.ChangeNext(objectFactory('TTT', self.screen, self.board, self.current_player))

    def draw_pause(self, screen):
        font = pg.font.Font(None, 50)
        pause = font.render("Game Paused", 1, (0, 0, 0))
        pause_rect = pause.get_rect(center=(900/2, 600/2))
        self.pause_message_rect = pg.Rect(900/2-200, 600/2-150/2, 400,150)
        pg.draw.rect(screen, (0,0,220), self.pause_message_rect)
        screen.blit(pause, pause_rect)

    def Draw(self, screen):
        if self.redraw == True:
            self.draw_pause(screen)
            self.redraw = False