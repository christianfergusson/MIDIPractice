'''
TODO
'''

import random

import pygame

import constants as c

pygame.init()

class NoteClass:

    BLACK_KEY_MODS = [1, 3, 6, 8, 10]
    NOTE_LETTERS = ["C", "D", "E", "F", "G", "A", "B"]

    def __init__(self, staff):
        self.staff = staff
        self.x = 0
        self.y = 0
        self.note_value = 0
        self.accidental = 0
        self.note_height = 0
        self.stem_up = True
        self.note_letter = ""
        self.generate_note_value()
        self.generate_note_height()
        self.generate_note_letter()
    
    def generate_note_value(self):
        self.note_value = random.randint(64,79)
        if self.staff.use_accidentals == True:
            if self.note_value % 12 in NoteClass.BLACK_KEY_MODS:
                self.accidental = random.choice([-1,1])
        else:
            while self.note_value % 12 in NoteClass.BLACK_KEY_MODS:
                self.note_value = random.randint(64,79)
    
    def generate_note_height(self):
        # Distance on staff from Middle C (60)
        black_keys_subtracted = len([i for i in NoteClass.BLACK_KEY_MODS if i <= self.note_value%12])
        self.note_height = self.note_value - black_keys_subtracted - (self.note_value//12 - 5)*5 - 60
        if self.accidental < 0:
            self.note_height += 1
        if self.note_height > 5:
            self.stem_up = False

    def generate_note_letter(self):
        accidental_letter = ""
        if self.accidental < 0:
            accidental_letter = "b"
        elif self.accidental > 0:
            accidental_letter = "#"
        self.note_letter = NoteClass.NOTE_LETTERS[self.note_height % 7] + accidental_letter
    
    def add_accidental(self):
        natural = True if random.randint(0, 100) < 62 else False
        if natural == False:
            self.accidental = random.choice([-1,1])
        if self.note_value % 12 not in NoteClass.BLACK_KEY_MODS:
            if self.accidental < 0:
                self.note_value -= 1
            elif self.accidental > 0:
                self.note_value += 1
        self.generate_note_height()
        self.generate_note_letter()

    def remove_accidental(self):
        if self.note_value % 12 in NoteClass.BLACK_KEY_MODS:
            if self.accidental < 0:
                self.note_value += 1
            elif self.accidental > 0:
                self.note_value -= 1
        self.accidental = 0
        self.generate_note_height()
        self.generate_note_letter()
        
    def update_note_positions(self, note_index):
        self.x = self.staff.array_x + note_index * self.staff.note_spacing
        self.y = self.note_height + 7
    
    def scale(self):
        pass
    
    def render(self, note_type):
        # Accidentals
        if self.accidental < 0:
            self.staff.screen.win.blit(self.staff.flat_img,
                (int((self.x-2.2)*self.staff.screen.x_percent),
                int((self.staff.y-(self.y-4.6)*self.staff.note_size)*self.staff.screen.y_percent)))
        if self.accidental > 0:
            self.staff.screen.win.blit(self.staff.sharp_img,
                (int((self.x-1.9)*self.staff.screen.x_percent),
                  int((self.staff.y-(self.y-5)*self.staff.note_size)*self.staff.screen.y_percent)))
        if note_type == "Whole":
            self.staff.screen.win.blit(self.staff.whole_note_img,
                 (int((self.x)*self.staff.screen.x_percent),
                  int((self.staff.y-(self.y)*self.staff.note_size)*self.staff.screen.y_percent)))
        elif note_type == "Half":
            if self.stem_up == True:
                self.staff.screen.win.blit(self.staff.half_note_up_img,
                    (int((self.x)*self.staff.screen.x_percent),
                    int((self.staff.y-(self.y)*self.staff.note_size)*self.staff.screen.y_percent)))
            else:
                    self.staff.screen.win.blit(self.staff.half_note_down_img,
                    (int((self.x)*self.staff.screen.x_percent),
                    int((self.staff.y-(self.y - 5.9)*self.staff.note_size)*self.staff.screen.y_percent)))
        elif note_type == "Quarter":
            if self.stem_up == True:
                self.staff.screen.win.blit(self.staff.quarter_note_up_img,
                (int((self.x)*self.staff.screen.x_percent),
                int((self.staff.y-(self.y)*self.staff.note_size)*self.staff.screen.y_percent)))
            else:
                self.staff.screen.win.blit(self.staff.quarter_note_down_img,
                (int((self.x)*self.staff.screen.x_percent),
                int((self.staff.y-(self.y - 5.9)*self.staff.note_size)*self.staff.screen.y_percent)))
        else:
            pass
        
    def process_events(self, event):
        pass