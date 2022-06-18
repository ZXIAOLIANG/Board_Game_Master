from turtle import home
import pygame as pg
from pygame.locals import *

from utility import *
class Scene:
    def __init__(self):
        self.next_scene = self
    
    def HandleEvents(self, events):
        pass

    def Draw(self, screen):
        pass

    def ChangeNext(self, next_scene):
        self.next_scene = next_scene
    
    def Terminate(self):
        self.ChangeNext(None)

class TicTacToeScene(Scene):
    def __init__(self, screen, board=[[None]*3 for _ in range(3)], current_player=1, board_size=600):
        Scene.__init__(self)
        self.back_but_rect = None
        self.pause_but_rect = None
        self.restart_but_rect = None
        self.board_rect = None
        self.screen = screen
        self.board = board
        self.current_player = current_player
        self.board_size = board_size
        x_image = pg.image.load('x.png')
        o_image = pg.image.load('o.png')
        self.x_img = pg.transform.scale(x_image, (100,100))
        self.o_img = pg.transform.scale(o_image, (100,100))
        self.redraw = True
        self.new_step = False
        self.new_x = 0
        self.new_y = 0
        self.result = "Playing"
        self.Draw(screen)

    def HandleEvents(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                print("mouse clicked")
                mouse_pos = pg.mouse.get_pos()
                if self.back_but_rect.collidepoint(mouse_pos):
                    print("back to menu")
                    self.ChangeNext(MenuScene(self.screen))
                elif self.pause_but_rect.collidepoint(mouse_pos):
                    print("game paused")
                    self.ChangeNext(PauseScene(self.screen, self.board, self.current_player))
                elif self.restart_but_rect.collidepoint(mouse_pos):
                    print("game restart")
                    self.reset()
                elif self.board_rect.collidepoint(mouse_pos):
                    self.check_step(mouse_pos)

    def check_step(self, mouse_pos):
        x, y = mouse_pos
        if x < self.board_size/3:
            x_index = 0
        elif x < self.board_size*2/3:
            x_index = 1
        elif x <= self.board_size:
            x_index = 2

        if y < self.board_size/3:
            y_index = 0
        elif y < self.board_size*2/3:
            y_index = 1
        elif y <= self.board_size:
            y_index = 2

        if self.board[x_index][y_index] is None:
            # new step
            self.new_step = True
            self.new_x = x_index
            self.new_y = y_index
            if self.current_player == 1:
                self.board[x_index][y_index] = True
            else:
                self.board[x_index][y_index] = False
            self.result = self.check_win()
            if self.result != "Playing":
                self.ChangeNext(ResultScene(self.screen, self.result))

    def reset(self):
        self.current_player = 1
        self.board = [[None]*3 for _ in range(3)]
        self.redraw = True

    def check_win(self):
        for row in range(3):
            if self.board[row][0] is not None and self.board[row][0] == self.board[row][1] == self.board[row][2]:
                return "Player " + str(self.current_player) + " win!"

        for col in range(3):
            if self.board[0][col] is not None and self.board[0][col] == self.board[1][col] == self.board[2][col]:
                return "Player " + str(self.current_player) + " win!"

        if self.board[0][0] is not None and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return "Player " + str(self.current_player) + " win!"

        if self.board[0][2] is not None and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return "Player " + str(self.current_player) + " win!"
        # check for draw condition
        draw_condition = True
        for x in range(3):
            for y in range(3):
                if self.board[x][y] is None:
                    draw_condition = False
        if draw_condition:
            return "Draw!"
        return "Playing"

    def draw_game(self, screen):
        screen.fill((255,255,255))
        pg.draw.line(screen,(0,0,0),(0,0),(0, self.board_size),7)
        pg.draw.line(screen,(0,0,0),(self.board_size/3,0),(self.board_size/3, self.board_size),7)
        pg.draw.line(screen,(0,0,0),(self.board_size/3*2,0),(self.board_size/3*2, self.board_size),7)
        pg.draw.line(screen,(0,0,0),(self.board_size,0),(self.board_size, self.board_size),7)
        # Drawing horizontal lines
        pg.draw.line(screen,(0,0,0),(0,0),(self.board_size, 0),7)
        pg.draw.line(screen,(0,0,0),(0,self.board_size/3),(self.board_size, self.board_size/3),7)
        pg.draw.line(screen,(0,0,0),(0,self.board_size/3*2),(self.board_size, self.board_size/3*2),7)
        pg.draw.line(screen,(0,0,0),(0,self.board_size),(self.board_size, self.board_size),7)
        self.board_rect = pg.Rect(0,0,600,600)

        font = pg.font.Font(None, 50)
        self.pause_but_rect = draw_button(font, "PAUSE", screen, (255,0,0), (self.board_size+150, 150), self.board_size+4, 100, 300, 100)
        self.back_but_rect = draw_button(font, "BACK", screen, (220,220,220), (self.board_size+150, 250), self.board_size+4, 200, 300, 100)
        self.restart_but_rect = draw_button(font, "RESTART", screen, (220,220,0), (self.board_size+150, 350), self.board_size+4, 300, 300, 100)

        # restart = font.render("RESTART", 1, (0, 0, 0))
        # restart_rect = restart.get_rect(center=(self.board_size+150, 350))
        # self.restart_but_rect = pg.Rect(self.board_size+4, 300, 300,100)
        # pg.draw.rect(screen, (220,220,0), self.restart_but_rect)
        # screen.blit(restart, restart_rect)

        # display instruction
        screen.fill ((255, 255, 255), (self.board_size+4, 0, 300,100))
        font2 = pg.font.Font(None, 30)
        instruction = font2.render("Player " + str(self.current_player) + "'s turn", 1, (0, 0, 0))
        inst_rect = instruction.get_rect(center=(self.board_size+150, 50))
        screen.blit(instruction, inst_rect)

    def update_instruction(self, screen):
        if self.current_player == 1:
            self.current_player = 2
        elif self.current_player == 2:
            self.current_player = 1

        screen.fill ((255, 255, 255), (self.board_size+4, 0, 300,100))
        font2 = pg.font.Font(None, 30)
        instruction = font2.render("Player " + str(self.current_player) + "'s turn", 1, (0, 0, 0))
        inst_rect = instruction.get_rect(center=(self.board_size+150, 50))
        screen.blit(instruction, inst_rect)

    def draw_step(self, screen):
        if self.current_player == 1:
            screen.blit(self.x_img,(self.new_x*200+50, self.new_y*200+50))
        else:
            screen.blit(self.o_img,(self.new_x*200+50, self.new_y*200+50))

    def draw_previous_steps(self, screen):
        for x_index in range(3):
            for y_index  in range(3):
                if self.board[x_index][y_index] == True:
                    screen.blit(self.x_img,(x_index*200+50, y_index*200+50))
                elif self.board[x_index][y_index] == False:
                    screen.blit(self.o_img,(x_index*200+50, y_index*200+50))

    def Draw(self, screen):
        if self.redraw == True:
            print("redraw")
            self.draw_game(screen)
            self.draw_previous_steps(screen)
            self.redraw = False
        if self.new_step == True:
            print("new step")
            self.draw_step(screen)
            self.update_instruction(screen)
            self.new_step = False

        # pg.display.update()
class SelectGameScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self)
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
                        self.ChangeNext(TicTacToeScene(self.screen, [[None]*3 for _ in range(3)], 1))
                if option_clicked == False:
                    self.ChangeNext(MenuScene(self.screen))
                    
                

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
        


class MenuScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self)
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
                    self.ChangeNext(SelectGameScene(self.screen))

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

class ResultScene(Scene):
    def __init__(self, screen, result):
        Scene.__init__(self)
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
                    self.ChangeNext(TicTacToeScene(self.screen, [[None]*3 for _ in range(3)], 1))

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

class PauseScene(Scene):
    def __init__(self, screen, board, current_player):
        Scene.__init__(self)
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
                    self.ChangeNext(TicTacToeScene(self.screen, self.board, self.current_player))

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