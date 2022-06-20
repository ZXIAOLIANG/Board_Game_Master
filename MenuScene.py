from turtle import home
import pygame as pg
from pygame.locals import *

import RootScene
# import SelectGameScene
from utility import *

RS = RootScene.RootScene
# SGS = SelectGameScene.SelectGameScene

class MenuScene(RS):
    def __init__(self, screen):
        super().__init__()
        self.redraw = True
        self.start_but_rect = None
        self.screen = screen 
        self.Draw(screen)

    def HandleEvents(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.start_but_rect.collidepoint(mouse_pos):
                    print("select game clicked")
                    self.ChangeNext(objectFactory('SelectGame', self.screen))

    def draw_menu(self, screen):
        screen.fill((255,255,255)) # white
        font = pg.font.Font(None, 80)
        text = font.render("Board Game Master", 1, (0, 0, 0))
        font.set_italic(True)
        font.set_bold(True)
        # put the title at the center of the screen
        text_rect = text.get_rect(center=(900/2, 200))
        screen.blit(text, text_rect)

        font2 = pg.font.Font(None, 50)
        self.start_but_rect = draw_button(font2, "Select Game", screen, (0,255,0), (900/2, 300), 300, 270, 300, 60)

    def Draw(self, screen):
        if self.redraw == True:
            self.draw_menu(screen)
            self.redraw = False