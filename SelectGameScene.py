from turtle import home
import pygame as pg
from pygame.locals import *

import RootScene
# import TicTacToeScene
# import MenuScene
from utility import *

RS = RootScene.RootScene
# TS = TicTacToeScene.TicTacToeScene
# MS = MenuScene.MenuScene

class SelectGameScene(RS):
    def __init__(self, screen):
        super().__init__()
        self.redraw = True
        self.screen = screen
        self.options = ["Tic Tac Toe", "Gomoku"]
        self.option_but_list = []
        self.hovered_option = -1
        self.Draw(screen)

    def HandleEvents(self, events):
        mouse_pos = pg.mouse.get_pos()
        for i, option_but in enumerate(self.option_but_list):
            if option_but.collidepoint(mouse_pos):
                if i != self.hovered_option:
                    self.hovered_option = i
                    self.redraw = True

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                option_clicked = False
                for i, option_but in enumerate(self.option_but_list):
                    if option_but.collidepoint(mouse_pos):
                        option_clicked = True
                        self.ChangeNext(objectFactory('TTT', self.screen, [[None]*3 for _ in range(3)], 1))
                if option_clicked == False:
                    self.ChangeNext(objectFactory('Menu', self.screen))
                    
                

    def draw_drop_down_menu(self, screen):
        pg.draw.line(screen,(0,0,0),(300, 270+60),(300, 270+60*(len(self.options)+1)),7)
        pg.draw.line(screen,(0,0,0),(600, 270+60),(600, 270+60*(len(self.options)+1)),7)
        pg.draw.line(screen,(0,0,0),(300, 270+60*(len(self.options)+1)),(600, 270+60*(len(self.options)+1)),7)
        self.option_but_list = []
        for i, option in enumerate(self.options):
            font = pg.font.Font(None, 50)
            if i == self.hovered_option:
                color = (172, 216, 230) # light blue color
            else:
                color = (255, 255, 255)
            option_but_area = draw_button(font, option, screen, color, (900/2, 300+60*(i+1)), 300, 270 + 60*(i+1), 300, 60)
            self.option_but_list.append(option_but_area)

    def Draw(self, screen):
        if self.redraw == True:
            self.draw_drop_down_menu(screen)
            self.redraw = False
        