'''
TODO
'''

import pygame

import constants as c

pygame.init()

class ButtonClass:
    def __init__(self, screen, xywhs, text, bg_color, index=0):
        self.screen = screen
        self.x, self.y, self.w, self.h, self.s = xywhs
        self.text = str(text)
        self.bg_color = bg_color
        self.index = index

    def render(self):
        button_rect = pygame.draw.rect(self.screen.win,
                                       self.bg_color,
                                       (int(self.x*self.screen.x_percent),
                                       int((self.y+self.s*self.index)*self.screen.y_percent),
                                       int(self.w*self.screen.x_percent),
                                       int(self.h*self.screen.y_percent)))
        button_text = self.screen.basic_font.render(self.text, True, c.BLACK)
        button_text_rect = button_text.get_rect()
        button_text_rect.center = button_rect.center
        self.screen.win.blit(button_text, button_text_rect)

    def check(self, mouse_x, mouse_y):
        if (self.x)*self.screen.x_percent < mouse_x < (self.x+self.w)*self.screen.x_percent:
            if (self.y+self.s*self.index)*self.screen.y_percent < mouse_y < (self.y+self.h+self.s*self.index)*self.screen.y_percent:
                #print(f"{self.text} {self.index}")
                return True