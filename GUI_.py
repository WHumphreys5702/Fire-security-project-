import pygame
import sys
from picamera import *
from time import *
import pygame.camera
import os
import opencv_therm_cam
import shutil
import outputs

opencv_therm_cam.camera_read()
Pi = 3.14


class Menu():
    def __init__(self, screen):
        # screen parameter is so each time something is drawn
        # with pygame it has a place to be mapped on
        self.screen = screen
        self.x_offset = 50

    def cursor(self):
        return pygame.mouse.get_pos()
    
    def update_screen(self):
        # draws out whatever will be placed on the menu
        # starting from (0,0)
        self.screen.window.blit(self.screen.display, (0, 0))
        pygame.display.update()

class MainMenu(Menu):
    def __init__(self, screen):
        Menu.__init__(self, screen)
        self.Status_y = MID_HEIGHT + 30
        self.Livefeed_y = MID_HEIGHT + 50
        self.Gallery_y = MID_HEIGHT + 70
        self.Options_y = MID_HEIGHT + 90
        self.y_offset = 10

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.screen.display.fill(BLACK)
            self.screen.render_image("Firewatch.png", 2.1, MID_WIDTH, MID_HEIGHT-100, True)
            self.screen.draw_text('Firewatch', WHITE, 50, MID_WIDTH, MID_HEIGHT -230)
            self.screen.draw_text("Status", WHITE, 20, MID_WIDTH, self.Status_y)
            self.screen.draw_text("Live Feed", WHITE, 20, MID_WIDTH, self.Livefeed_y)
            self.screen.draw_text("Gallery", WHITE, 20, MID_WIDTH, self.Gallery_y)
            self.screen.draw_text("Options", WHITE, 20, MID_WIDTH, self.Options_y)
            self.update_screen()

    def check_input(self):
        mouse = self.cursor()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] in range(MID_WIDTH - self.x_offset, MID_WIDTH + self.x_offset):
                    if mouse[1] in range(self.Status_y - self.y_offset , self.Status_y + self.y_offset):
                        self.screen.curr_menu = self.screen.Status
                    elif mouse[1] in range(self.Livefeed_y - self.y_offset, self.Livefeed_y + self.y_offset):
                        self.screen.curr_menu = self.screen.LiveFeed
                    elif mouse [1] in range (self.Gallery_y - self.y_offset, self.Gallery_y + self.y_offset):
                        self.screen.curr_menu = self.screen.Gallery 
                    elif mouse[1] in range (self.Options_y - self.y_offset, self.Options_y + self.y_offset):
                        self.screen.curr_menu = self.screen.Options
                    self.run_display = False
                    
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

# Put Arc and Thermal Values

class Status(Menu):
    def __init__(self, screen):
        Menu.__init__(self, screen)
        
    def display_menu(self):
        self.run_display = True
        self.screen.display.fill(BLACK)
        while self.run_display:
            self.check_input()
            value = opencv_therm_cam.camera_read()
            self.screen.draw_text("Heat Data", WHITE, 50, MID_WIDTH, MID_HEIGHT - 200)
            pygame.draw.circle(self.screen.display, WHITE ,(MID_WIDTH,MID_HEIGHT),100) 
            pygame.draw.circle(self.screen.display, BLACK ,(MID_WIDTH,MID_HEIGHT),90)
            pygame.draw.arc(self.screen.display, RED , (200,200,200,200),Pi/2,(value*.0196),10)
            self.screen.draw_text(str(value) + " " + "*F", WHITE, 30, MID_WIDTH, MID_HEIGHT)     
            self.update_screen()
            
    def check_input(self):
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                            self.screen.curr_menu = self.screen.main_menu
                self.run_display = False

# This just opens the preview camera


class LiveFeed(Menu):
    def __init__(self, screen):
        Menu.__init__(self, screen)
        self.camera = PiCamera()

    def display_menu(self):
        self.run_display = True
        self.camera.start_preview()
        self.camera.resolution = (WIDTH, HEIGHT)
        while self.run_display:
            self.check_input()
            self.update_screen()
            
    def check_input(self):
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                            self.camera.stop_preview()
                            self.camera.close()
                            self.screen.curr_menu = self.screen.main_menu
                    self.run_display = False
                    self.camera = PiCamera()
class Gallery(Menu):

    def __init__(self, screen):
        Menu.__init__(self, screen)
        state = "Gallery_Main_Start"
        
    folder_dir = r"/home/pi/Final_project/Images"
    state = "Gallery_Main_Start"
    least = []
    most = []
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            if self.state == "Gallery_Main_Start":
                self.screen.display.fill(BLACK)
                x_counter = 0
                y_counter = 0
                x_text = 1
                y_text = 1
                for i in os.listdir(self.folder_dir):
                    imp = pygame.image.load(i).convert()
                    imp = pygame.transform.scale(imp,(1200/4,720/4))
                    self.screen.display.blit(imp, (x_counter*(300), y_counter*(200)))
                    des = str(i)
                    des = des[0:-4]
                    self.screen.draw_text(des, WHITE, 20, (x_text)*(158), (y_text)*(190+(2*y_text)))
                    self.least.append((x_counter*300,y_counter*180))
                    self.most.append((300+(x_counter*300),180+(y_counter*180)))
                    x_counter += 1
                    x_text += 2
                    if x_counter == 2:
                        y_counter += 1
                        y_text += 1
                        x_counter = 0
                        x_text = 1
                self.state = "Gallery_Main_Idle"

                
            self.update_screen()
            self.check_input(self.least, self.most)

    def check_input(self, least, most):
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            
            if self.state == "Gallery_Main_Idle":
                for i in range(len(least)):
                    file = os.listdir(self.folder_dir)[i]        
                    if least[i][0] <= mouse[0] and mouse[0] <= most[i][0] and least[i][1] <= mouse[1] and mouse[1] <= most[i][1]:
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            self.screen.display.fill(BLACK)               
                            imp = pygame.image.load(file).convert()
                            imp = pygame.transform.scale(imp,(600,600))
                            self.screen.display.blit(imp,(0,0))
                            self.state = "Gallery_Image"
                            self.least = []
                            self.most = []

               
                        if ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_TAB:
                                if least[i][0] <= mouse[0] and mouse[0] <= most[i][0] and least[i][1] <= mouse[1] and mouse[1] <= most[i][1]:
                                    os.remove(file)
                                    second = self.folder_dir + "//" + file
                                    os.remove(second)
                                    del self.least[i]
                                    del self.most[i]
                                    self.state = "Gallery_Main_Start"
                                    self.least = []
                                    self.most = []
                                    break
                    
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_SPACE:
                        self.state = "Gallery_Main_Start"
                        self.least = []
                        self.most = []
                        self.screen.curr_menu = self.screen.main_menu
                        self.run_display = False       



            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    if self.state == "Gallery_Main_Idle":
                        self.state = "Gallery_Main_Start"
                        self.least = []
                        self.most = []
                        self.screen.curr_menu = self.screen.main_menu
                        self.run_display = False

            if self.state == "Gallery_Image":
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.state = "Gallery_Main_Start"



        
        


# Template for the other menus
# Need to make each thing its own button
# and have a way to save it in a text file

class Options(Menu):
    def __init__(self, screen):
        Menu.__init__(self, screen)
        self.Change_Number_y = MID_HEIGHT - 90
        self.Change_Email_y = MID_HEIGHT + 5
        self.Change_Address_y = MID_HEIGHT + 90 

    state = "Options_Main"
    line = ""
    current_edit = ""
    user_text = ""
                    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.screen.display.fill(BLACK)
            if self.state == "Options_Main":
                self.check_input()
                self.screen.draw_text('Change Number', WHITE, 40, MID_WIDTH, self.Change_Number_y)
                self.screen.draw_text('Change Email', WHITE, 40, MID_WIDTH, self.Change_Email_y)
                self.screen.draw_text('Change Address', WHITE, 40, MID_WIDTH, self.Change_Address_y)
            if self.state == "Options_Configurations":
                self.check_input(False,self.line)
                self.screen.draw_text("Now changing " + self.current_edit + "...", WHITE, 30,MID_WIDTH, MID_HEIGHT-200)
                self.screen.draw_text(self.user_text, WHITE, 30,MID_WIDTH, MID_HEIGHT)
                self.update_screen()
            self.update_screen()
            
    def check_input(self, main = True, line = None):
        for ev in pygame.event.get():
                if main:
                    mouse = self.cursor()
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if mouse[0] in range(MID_WIDTH - 4 * self.x_offset, MID_WIDTH + 4 * self.x_offset):
                            if mouse[1] in range(192,224):
                                self.line = 0
                                self.current_edit = "number"
                            if mouse[1] in range(290,321):
                                self.line = 1
                                self.current_edit = "email"
                            if mouse[1] in range(316,396):
                                self.line = 2
                                self.current_edit = "address"
                            self.state = "Options_Configurations"
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_ESCAPE:
                            self.screen.curr_menu = self.screen.main_menu
                            self.run_display = False
                else:
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[0:-1]
                        if ev.key == pygame.K_RETURN:
                            # if a user hits the escape key without adding anything
                            # else it will break the formatting of txt file
                            if len(self.user_text) > 2:
                                outputs.write(self.user_text, self.line)
                            self.reset_input()
                        if ev.key == pygame.K_ESCAPE:
                            self.reset_input()
                        else:
                            # without this conditional statement a user could input a backspace ASCII character
                            # which would break the entire program
                            if ev.key != pygame.K_BACKSPACE:
                                self.user_text += ev.unicode  

                    
    def reset_input(self):
        self.user_text = ""
        self.state = "Options_Main"



# Main Class

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Firewatch")
        self.display = pygame.Surface((WIDTH,HEIGHT))
        self.window = pygame.display.set_mode(((WIDTH,HEIGHT)))
        self.main_menu = MainMenu(self)
        self.Status = Status(self)
        self.LiveFeed = LiveFeed(self)
        self.Gallery = Gallery(self)
        self.Options = Options(self)
        self.curr_menu = self.main_menu

    def draw_text(self, text, color, size, x, y ):
        # takes the font and its size
        font = pygame.font.Font(general,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)


    def render_image(self, image, scale, center_x, center_y, Center = True, full_screen = False, starting_x = None, starting_y = None):
        # gui classes was done by different group members hence two different methods of rendering an image
        # when you want to display an image by its middle x and y position
        if Center:
            pic = pygame.image.load(image)
            rect = pic.get_rect()
            if full_screen:
                pic = pygame.transform.scale(pic,(WIDTH,HEIGHT))
            else:
                pic = pygame.transform.scale(pic,(rect.w/scale,rect.h/scale))
            rect = pic.get_rect()
            rect.center = (center_x,center_y)
            self.display.blit(pic, (rect))
        # when you want to display an image by its starting x and y position
        else:
            pic = pygame.image.load(image)
            rect = pic.get_rect
            #pic = pygame.transform.scale(pic,(rect.w/scale,rect.h/scale))
            self.display.blit(pic,(starting_x, starting_y))
        
   
########################################################################################
#                                       MAIN
########################################################################################

# Dimensions for the window
WIDTH =  600
HEIGHT = 600

# Since most of our text is centered
MID_WIDTH = WIDTH // 2
MID_HEIGHT = HEIGHT // 2

# RGB values for text colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

# Can set any font here and the program will run fine
general = pygame.font.get_default_font()

# program is on idle mode until it detects a heat signature then pulls up GUI
#opencv_therm_cam.camera_read()
    
g = Game()

while True:
    g.curr_menu.display_menu()
