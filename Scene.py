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

class GameScene(Scene):
    def __init__(self, screen, line_width, board_offset, block_count, current_player=1, board_size=600):
        Scene.__init__(self)
        self.screen = screen
        self.pause_but_rect = None
        self.back_but_rect = None
        self.restart_but_rect = None
        self.current_player = current_player
        self.line_width = line_width
        self.board_offset = board_offset
        self.block_count = block_count
        self.board_size = board_size
        self.redraw = True
        self.new_step = False
        self.new_x = 0
        self.new_y = 0
        self.result = "Playing"
        self.steps = 0

    def draw_game(self, screen):
        screen.fill((255,255,255)) # fill the whole window with white: remove the previous scene
        screen.fill((222,184,135), (0, 0, self.board_size, self.board_size))

        block_size = calculate_block_size(self.board_size, self.board_offset, self.block_count)

        for i in range(self.block_count+1):
            pg.draw.line(screen, (0, 0, 0), (self.board_offset, self.board_offset + block_size * i), (self.board_size - self.board_offset, self.board_offset + block_size * i), self.line_width)
            pg.draw.line(screen, (0, 0, 0), (self.board_offset + block_size * i, self.board_offset), (self.board_offset + block_size * i, self.board_size - self.board_offset), self.line_width)
        
        self.board_rect = pg.Rect(0,0,self.board_size,self.board_size)

        font = pg.font.Font(None, 50)
        self.pause_but_rect = draw_button(font, "PAUSE", screen, (255,0,0), (self.board_size+150, 150), self.board_size+self.line_width, 100, 300, 100)
        self.back_but_rect = draw_button(font, "BACK", screen, (220,220,220), (self.board_size+150, 250), self.board_size+self.line_width, 200, 300, 100)
        self.restart_but_rect = draw_button(font, "RESTART", screen, (220,220,0), (self.board_size+150, 350), self.board_size+self.line_width, 300, 300, 100)

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

class TicTacToeScene(GameScene):
    def __init__(self, screen, board=[[None]*3 for _ in range(3)], current_player=1):
        GameScene.__init__(self, screen, 7, 0, 3, current_player)
        self.board_rect = None
        self.board = board
        x_image = pg.image.load('x.png')
        o_image = pg.image.load('o.png')
        self.x_img = pg.transform.scale(x_image, (100,100))
        self.o_img = pg.transform.scale(o_image, (100,100))

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
                    self.ChangeNext(PauseScene(self.screen, self.board, self.current_player, "TicTacToe"))
                elif self.restart_but_rect.collidepoint(mouse_pos):
                    print("game restart")
                    self.reset()
                elif self.board_rect.collidepoint(mouse_pos):
                    self.check_step(mouse_pos)

    def check_step(self, mouse_pos):
        x, y = mouse_pos
        if x != 600:
            x_index = x // 200
        else:
            x_index = 2
        
        if y != 600:
            y_index = y // 200
        else:
            y_index = 2

        if self.board[x_index][y_index] is None:
            # new step
            self.new_step = True
            self.new_x = x_index
            self.new_y = y_index
            self.steps += 1
            if self.current_player == 1:
                self.board[x_index][y_index] = True
            else:
                self.board[x_index][y_index] = False
            self.result = self.check_win()
            if self.result != "Playing":
                self.ChangeNext(ResultScene(self.screen, self.result, "TicTacToe"))

    def reset(self):
        self.current_player = 1
        self.board = [[None]*3 for _ in range(3)]
        self.redraw = True

    def check_win(self):
        last_move_color = self.board[self.new_x][self.new_y]
        connected_pieces = check_horizontal_connection(self.board, last_move_color, self.new_x, self.new_y, 3, 3)
        if connected_pieces >= 3:
            return "Player " + str(self.current_player) + " win!"

        connected_pieces = check_vertical_connection(self.board, last_move_color, self.new_x, self.new_y, 3, 3)
        if connected_pieces >= 3:
            return "Player " + str(self.current_player) + " win!"

        connected_pieces = check_main_diagnal_connection(self.board, last_move_color, self.new_x, self.new_y, 3, 3)
        if connected_pieces >= 3:
            return "Player " + str(self.current_player) + " win!"

        connected_pieces = check_inverse_diagnal_connection(self.board, last_move_color, self.new_x, self.new_y, 3, 3)
        if connected_pieces >= 3:
            return "Player " + str(self.current_player) + " win!"
        
        # check for draws
        if self.steps == 3*3:
            return "Draw"
        print("yes")
        return "Playing"

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

class GomokuScene(GameScene):
    def __init__(self, screen, board=[[None]*15 for _ in range(15)], current_player=1):
        GameScene.__init__(self, screen, 5, 20, 14, 1)
        self.board_rect = None
        self.board = board
        self.current_player = current_player
        x_image = pg.image.load('black600.png')
        o_image = pg.image.load('white600.png')
        self.x_img = pg.transform.scale(x_image, (30,30))
        self.o_img = pg.transform.scale(o_image, (30,30))

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
                    self.ChangeNext(PauseScene(self.screen, self.board, self.current_player, "Gomoku"))
                elif self.restart_but_rect.collidepoint(mouse_pos):
                    print("game restart")
                    self.reset()
                elif self.board_rect.collidepoint(mouse_pos):
                    self.check_step(mouse_pos)

    def check_step(self, mouse_pos):
        x, y = mouse_pos
        block_size = calculate_block_size(self.board_size, self.board_offset, self.block_count)

        if x != self.board_size:
            x_index = int(x// block_size)
        else:
            x_index = int(self.block_count)
        if y!= 600:
            y_index = int(y//block_size)
        else:
            y_index = int(self.block_count)

        if self.board[x_index][y_index] is None:
            # new step
            self.new_step = True
            self.steps += 1
            self.new_x = x_index
            self.new_y = y_index
            if self.current_player == 1:
                self.board[x_index][y_index] = True
            else:
                self.board[x_index][y_index] = False
            self.result = self.check_win()
            if self.result != "Playing":
                self.ChangeNext(ResultScene(self.screen, self.result, "Gomoku"))

    def reset(self):
        self.current_player = 1
        self.board = [[None]*15 for _ in range(15)]
        self.redraw = True

    def check_win(self):
        last_move_color = self.board[self.new_x][self.new_y]
        connected_pieces = check_horizontal_connection(self.board, last_move_color, self.new_x, self.new_y, 5, 15)
        if connected_pieces >= 5:
            return "Player " + str(self.current_player) + " win!"

        connected_pieces = check_vertical_connection(self.board, last_move_color, self.new_x, self.new_y, 5, 15)
        if connected_pieces >= 5:
            return "Player " + str(self.current_player) + " win!"

        connected_pieces = check_main_diagnal_connection(self.board, last_move_color, self.new_x, self.new_y, 5, 15)
        if connected_pieces >= 5:
            return "Player " + str(self.current_player) + " win!"

        connected_pieces = check_inverse_diagnal_connection(self.board, last_move_color, self.new_x, self.new_y, 5, 15)
        if connected_pieces >= 5:
            return "Player " + str(self.current_player) + " win!"
        
        # check for draw
        if self.steps == 15*15:
            return "Draw"
        
        return "Playing"

    def draw_step(self, screen):
        if self.current_player == 1:
            screen.blit(self.x_img,(self.new_x*40+5, self.new_y*40+5))
        else:
            screen.blit(self.o_img,(self.new_x*40+5, self.new_y*40+5))

    def draw_previous_steps(self, screen):
        for x_index in range(15):
            for y_index  in range(15):
                if self.board[x_index][y_index] == True:
                    screen.blit(self.x_img,(x_index*40+5, y_index*40+5))
                elif self.board[x_index][y_index] == False:
                    screen.blit(self.o_img,(x_index*40+5, y_index*40+5))

class SelectGameScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self)
        self.redraw = True
        self.screen = screen
        self.options = ["Tic Tac Toe", "Gomoku"]
        self.option_but_list = []
        self.hovered_option = -1
        # self.Draw(screen)

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
                    if option_but.collidepoint(mouse_pos) and i==0:
                        option_clicked = True
                        self.ChangeNext(TicTacToeScene(self.screen, [[None]*3 for _ in range(3)], 1))
                    elif option_but.collidepoint(mouse_pos) and i==1:
                        option_clicked = True
                        self.ChangeNext(GomokuScene(self.screen, [[None]*15 for _ in range(15)], 1))
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
        # self.Draw(screen)

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
    def __init__(self, screen, result, game):
        Scene.__init__(self)
        self.redraw = True
        self.result_message_rect = None
        self.screen = screen 
        self.result = result
        self.game = game
        # self.Draw(screen)

    def HandleEvents(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.result_message_rect.collidepoint(mouse_pos):
                    if self.game == "TicTacToe":
                        self.ChangeNext(TicTacToeScene(self.screen, [[None]*3 for _ in range(3)], 1))
                    elif self.game == "Gomoku":
                        self.ChangeNext(GomokuScene(self.screen, [[None]*15 for _ in range(15)], 1))

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
    def __init__(self, screen, board, current_player, game):
        Scene.__init__(self)
        self.redraw = True
        self.pause_message_rect = None
        self.screen = screen 
        self.board = board
        self.current_player = current_player
        self.game = game
        # self.Draw(screen)

    def HandleEvents(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.pause_message_rect.collidepoint(mouse_pos):
                    if self.game == "TicTacToe":
                        self.ChangeNext(TicTacToeScene(self.screen, self.board, self.current_player))
                    elif self.game == "Gomoku":
                        self.ChangeNext(GomokuScene(self.screen, self.board,self.current_player))

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