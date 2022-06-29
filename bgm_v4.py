import pygame as pg
from pygame.locals import *
import sys
from Scene import *


class Board_Game_Master():
    def __init__(self, fps, window_width, window_height):
        pg.init()
        self.fps = fps
        self.cl = pg.time.Clock()
        self.screen = pg.display.set_mode((window_width, window_height), 0, 32)
        pg.display.set_caption("Board Game Master")
        self.scene = MenuScene(self.screen)
        self.scene.Draw(self.screen)

    def gameloop(self):
        pg.event.clear()
        # run the game loop forever
        while True:
            events = []
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                else:
                    events.append(event)
            self.scene.HandleEvents(events)
            self.scene.Draw(self.screen)
            self.scene = self.scene.next_scene
            self.scene.Draw(self.screen)
                    
            pg.display.update()
            self.cl.tick(self.fps)

if __name__ == "__main__":
    bgm = Board_Game_Master(30, 900, 600)
    bgm.gameloop()
