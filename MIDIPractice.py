'''
TODO Implement error handling for no MIDI device
xTODO Fix scaling
xTODO Fix ledger line positions
xTODO Fix speed scaling to match BPM
xTODO Add accidentals
TODO Consolidate user var strings into lists (to index through)
xTODO Add images for clefs
xTODO Add images for notes
xTODO Add images for accidentals
TODO Restructure scaling (https://www.pygame.org/wiki/WindowResizing)
TODO Limit resizing ratio to prevent x-scale squish
TODO Add contols for:
        Setting speed (BPM)
        Setting note spacing
        Selecting staves
        Using accidentals
        Showing note letter
        Changing note type
        -
        Adjusting note range
        Merging/splitting staves
xTODO Add note stems
TODO Add automatic speed scaling (+ and/or -) for position value reaching threshold
TODO Align image files around an origin (if you find time)
TODO Restructure project
'''



'''
DEV NOTES:

Piano range is from 21-108
Middle C is 60
'''

import time
import random
import pygame, sys
import pygame.gfxdraw
from pygame.locals import *
from pygame import midi

import os
os.system('cls' if os.name == 'nt' else 'clear')



pygame.init()
MONITOR_RESOLUTION = pygame.display.Info()
#win = pygame.display.set_mode((MONITOR_RESOLUTION.current_w, MONITOR_RESOLUTION.current_h), pygame.FULLSCREEN)
win = pygame.display.set_mode((800, 600), pygame.RESIZABLE)


title_bar = 'Sight Reading Practice'
pygame.display.set_caption(title_bar)
FRAMERATE = 60
fps_clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

win.fill(WHITE)



class Staff():

    NOTE_SIZE = 2
    TREBLE_MIDDLE_C_YLOC = 35
    BASS_MIDDLE_C_YLOC = 45
    STAFF_XLOC = 6
    GOAL_XLOC = 26

    winx = None
    winy = None
    x_percent = None
    y_percent = None

    basic_font = None
    symbol_font = None
    
    treble_clef_ratio = 323/118
    treble_clef_img = pygame.image.load("graphics/treble_clef.png").convert_alpha()
    bass_clef_ratio = 150/130
    bass_clef_img = pygame.image.load("graphics/bass_clef.png").convert_alpha()
    sharp_ratio = 142/45
    sharp_img = pygame.image.load("graphics/sharp.png").convert_alpha()
    flat_ratio = 106/43
    flat_img = pygame.image.load("graphics/flat.png").convert_alpha()
    whole_note_ratio = 48/79
    whole_note_img = pygame.image.load("graphics/whole_note.png").convert_alpha()
    half_note_ratio = 188/62
    half_note_up_img = pygame.image.load("graphics/half_note.png").convert_alpha()
    half_note_down_img = pygame.image.load("graphics/half_note.png").convert_alpha()
    quarter_note_ratio = 188/62
    quarter_note_up_img = pygame.transform.rotate(pygame.image.load("graphics/quarter_note.png").convert_alpha(),180)
    quarter_note_down_img = pygame.transform.rotate(pygame.image.load("graphics/quarter_note.png").convert_alpha(),180)

    old_winx = 0
    old_winy = 0


    
    def __init__(self):
        Staff.scale()

        # User variables
        self.BPM = 120
        self.note_spacing = 12
        self.staves = "Treble"
        self.use_accidentals = False
        self.show_letter = False
        self.show_MIDI = True
        self.note_type = "Whole"
        ##
        
        self.note_list = []
        self.add_notes()
            
        self.show_stem = False

        self.position = 100 + Staff.NOTE_SIZE
        
        self.highest_note = 64
        self.lowest_note = 57

        self.symbol_correct = False
        self.symbol_speed = 12
        self.symbol_timer = 0
        self.symbol_alpha = 0

    
    def scale():
        Staff.winx, Staff.winy = win.get_size()
        if Staff.winx != Staff.old_winx or Staff.winy != Staff.old_winy:
            #if Staff.winy > Staff.winx*4:
                #win = pygame.display.set_mode((Staff.winy/4, Staff.winy), pygame.RESIZABLE)
            Staff.old_winx = Staff.winx
            Staff.old_winy = Staff.winy
            Staff.x_percent = Staff.winx/100
            Staff.y_percent = Staff.winy/100
            Staff.basic_font = pygame.font.SysFont('Calibri', int(4*Staff.y_percent))
            Staff.accidental_font = pygame.font.SysFont('Calibri', int(6*Staff.y_percent))
            Staff.symbol_font = pygame.font.SysFont('Calibri', int(8*Staff.y_percent), bold=True)
            Staff.treble_clef_img = pygame.image.load("graphics/treble_clef.png").convert_alpha()
            Staff.bass_clef_img = pygame.image.load("graphics/bass_clef.png").convert_alpha()
            Staff.sharp_img = pygame.image.load("graphics/sharp.png").convert_alpha()
            Staff.flat_img = pygame.image.load("graphics/flat.png").convert_alpha()
            Staff.whole_note_img = pygame.image.load("graphics/whole_note.png").convert_alpha()
            Staff.half_note_up_img = pygame.image.load("graphics/half_note.png").convert_alpha()
            Staff.half_note_down_img = pygame.transform.rotate(pygame.image.load("graphics/half_note.png").convert_alpha(),180)
            Staff.quarter_note_up_img = pygame.image.load("graphics/quarter_note.png").convert_alpha()
            Staff.quarter_note_down_img = pygame.transform.rotate(pygame.image.load("graphics/quarter_note.png").convert_alpha(),180)
            Staff.treble_clef_img = pygame.transform.scale(Staff.treble_clef_img, (int(10*Staff.y_percent),int(10*Staff.y_percent*Staff.treble_clef_ratio)))
            Staff.bass_clef_img = pygame.transform.scale(Staff.bass_clef_img, (int(12*Staff.y_percent),int(12*Staff.y_percent*Staff.bass_clef_ratio)))
            Staff.sharp_img = pygame.transform.scale(Staff.sharp_img, (int(2.5*Staff.y_percent),int(2.5*Staff.y_percent*Staff.sharp_ratio)))
            Staff.flat_img = pygame.transform.scale(Staff.flat_img, (int(3*Staff.y_percent),int(3*Staff.y_percent*Staff.flat_ratio)))
            Staff.whole_note_img = pygame.transform.scale(Staff.whole_note_img, (int(7*Staff.y_percent),int(7*Staff.y_percent*Staff.whole_note_ratio)))
            Staff.half_note_up_img = pygame.transform.scale(Staff.half_note_up_img, (int(5*Staff.y_percent),int(5*Staff.y_percent*Staff.half_note_ratio)))
            Staff.half_note_down_img = pygame.transform.scale(Staff.half_note_down_img, (int(5*Staff.y_percent),int(5*Staff.y_percent*Staff.half_note_ratio)))
            Staff.quarter_note_up_img = pygame.transform.scale(Staff.quarter_note_up_img, (int(5*Staff.y_percent),int(5*Staff.y_percent*Staff.quarter_note_ratio)))
            Staff.quarter_note_down_img = pygame.transform.scale(Staff.quarter_note_down_img, (int(5*Staff.y_percent),int(5*Staff.y_percent*Staff.quarter_note_ratio)))

    
    def add_notes(self):
        self.note_qty = int(100/self.note_spacing)
        if len(self.note_list) < self.note_qty:
            for i in range(self.note_qty):
                self.note_list.append(Note(self.use_accidentals))
                #print(self.note_list[i].note_value)
        elif len(self.note_list) > self.note_qty:
            self.note_list = self.note_list[0:self.note_qty]

    def update_note_position(self):
        if self.position > Staff.GOAL_XLOC:
            self.position = max(self.position-(self.note_spacing/FRAMERATE*(self.BPM/FRAMERATE)), Staff.GOAL_XLOC)
    
    def render(self):
        self.render_staff()
        self.render_notes()
        self.render_symbol()
        self.render_options()
    
    def render_options(self):

        BPM_choice = Staff.basic_font.render("BPM:  " + str(self.BPM), True, BLACK)
        win.blit(BPM_choice, (int((25)*Staff.x_percent), int((85)*Staff.y_percent)))

        note_spacing_choice = Staff.basic_font.render("Spacing:  " + str(self.note_spacing), True, BLACK)
        win.blit(note_spacing_choice, (int((25)*Staff.x_percent), int((90)*Staff.y_percent)))

        staff_choice_text = "Staff:  " + self.staves
        staff_choice = Staff.basic_font.render(staff_choice_text, True, BLACK)
        win.blit(staff_choice, (int((25)*Staff.x_percent), int((95)*Staff.y_percent)))

        accidental_choice_text = "Accidentals:  Yes" if self.use_accidentals else "Accidentals:  No"
        accidental_choice = Staff.basic_font.render(accidental_choice_text, True, BLACK)
        win.blit(accidental_choice, (int((55)*Staff.x_percent), int((85)*Staff.y_percent)))

        letter_choice_text = "Note Letter:  Show" if self.show_letter else "Note Letter:  Hide"
        letter_choice = Staff.basic_font.render(letter_choice_text, True, BLACK)
        win.blit(letter_choice, (int((55)*Staff.x_percent), int((90)*Staff.y_percent)))

        note_choice = Staff.basic_font.render("Note:  " + self.note_type, True, BLACK)
        win.blit(note_choice, (int((55)*Staff.x_percent), int((95)*Staff.y_percent)))
    
    def render_staff(self):
        # Staves
        for i in range(5):
            pygame.draw.rect(win,
                             BLACK,
                             (int(Staff.STAFF_XLOC*Staff.x_percent),
                              int((Staff.TREBLE_MIDDLE_C_YLOC-(i+1)*Staff.NOTE_SIZE*2)*Staff.y_percent),
                              int((100)*Staff.x_percent),
                              2))
        for i in range(5):
            pygame.draw.rect(win,
                             BLACK,
                             (int(Staff.STAFF_XLOC*Staff.x_percent),
                              int((Staff.BASS_MIDDLE_C_YLOC+(i+1)*Staff.NOTE_SIZE*2)*Staff.y_percent),
                              int((100)*Staff.x_percent),
                              2))
            
        # Clefs
        win.blit(Staff.treble_clef_img,
                 (int((Staff.STAFF_XLOC+2)*Staff.x_percent),
                  int((Staff.TREBLE_MIDDLE_C_YLOC-25)*Staff.y_percent)))
        win.blit(Staff.bass_clef_img,
                 (int((Staff.STAFF_XLOC+2)*Staff.x_percent),
                  int((Staff.BASS_MIDDLE_C_YLOC+4)*Staff.y_percent)))
        
        # Goal Lines
        pygame.draw.rect(win,
                         BLACK,
                         (int((Staff.STAFF_XLOC+13)*Staff.x_percent),
                          int((Staff.TREBLE_MIDDLE_C_YLOC-Staff.NOTE_SIZE*10)*Staff.y_percent),
                          2,
                          int((Staff.NOTE_SIZE*8)*Staff.y_percent)))
        pygame.draw.rect(win,
                         BLACK,
                         (int((Staff.STAFF_XLOC+13)*Staff.x_percent),
                          int((Staff.BASS_MIDDLE_C_YLOC+Staff.NOTE_SIZE*2)*Staff.y_percent),
                          2,
                          int((Staff.NOTE_SIZE*8)*Staff.y_percent)))

    def render_notes(self):
        for index, note in enumerate(self.note_list):
            note_xloc = self.position+index*self.note_spacing

            # Note Value
            if self.show_MIDI == True:
                note_num = Staff.basic_font.render(str(note.note_value), True, BLUE)
                note_num_rect = note_num.get_rect(center=(int((note_xloc)*Staff.x_percent), int((2)*Staff.y_percent)))
                win.blit(note_num, note_num_rect)

            # Note Letter
            if self.show_letter == True:
                note_letter = Staff.basic_font.render(str(note.note_letter), True, BLUE)
                note_letter_rect = note_letter.get_rect(center=(int((note_xloc)*Staff.x_percent), int((2)*Staff.y_percent + 20)))
                win.blit(note_letter, note_letter_rect)

            # Ledger Lines
            if note.note_value >= 50:
                if note.note_height < 1:
                    for ledgerLine in range((2-note.note_height)//2):
                        pygame.draw.rect(win,
                                         BLACK,
                                         (int((note_xloc-2)*Staff.x_percent),
                                          int((Staff.TREBLE_MIDDLE_C_YLOC+(ledgerLine*2)*Staff.NOTE_SIZE)*Staff.y_percent),
                                          int((Staff.NOTE_SIZE*2)*Staff.x_percent),
                                          2))
                if note.note_height > 11:
                    for ledgerLine in range((note.note_height-10)//2):
                        pygame.draw.rect(win,
                                         BLACK,
                                         (int((note_xloc-2)*Staff.x_percent),
                                          int((Staff.TREBLE_MIDDLE_C_YLOC-(12*Staff.NOTE_SIZE)-(ledgerLine*2)*Staff.NOTE_SIZE)*Staff.y_percent),
                                          int((Staff.NOTE_SIZE*2)*Staff.x_percent),
                                          2))
            
            # Note
            if self.note_type == "Whole":
                win.blit(Staff.whole_note_img,
                 (int((note_xloc-2.5)*Staff.x_percent),
                  int((Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height+1)*Staff.NOTE_SIZE)*Staff.y_percent)))
            elif self.note_type == "Half":
                if note.stem_up == True:
                    win.blit(Staff.half_note_up_img,
                    (int((note_xloc-2)*Staff.x_percent),
                    int((Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height+6.4)*Staff.NOTE_SIZE)*Staff.y_percent)))
                else:
                    win.blit(Staff.half_note_down_img,
                    (int((note_xloc-2)*Staff.x_percent),
                    int((Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height+1.1)*Staff.NOTE_SIZE)*Staff.y_percent)))
            elif self.note_type == "Quarter":
                if note.stem_up == True:
                    win.blit(Staff.quarter_note_up_img,
                    (int((note_xloc-2)*Staff.x_percent),
                    int((Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height+6.4)*Staff.NOTE_SIZE)*Staff.y_percent)))
                else:
                    win.blit(Staff.quarter_note_down_img,
                    (int((note_xloc-2)*Staff.x_percent),
                    int((Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height+1.1)*Staff.NOTE_SIZE)*Staff.y_percent)))
            else:
                pygame.gfxdraw.filled_circle(win,
                                         int((note_xloc)*Staff.x_percent),
                                         int((Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height)*Staff.NOTE_SIZE)*Staff.y_percent),
                                         int((Staff.NOTE_SIZE)*Staff.y_percent),
                                         note.note_color)
                    
            # Accidentals
            if note.accidental < 0:
                win.blit(Staff.flat_img,
                 (int((note_xloc-5)*Staff.x_percent),
                  int((Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height+2.3)*Staff.NOTE_SIZE)*Staff.y_percent)))
                #flat_symbol = Staff.accidental_font.render("b", True, note.note_color)
                #flat_symbol_rect = flat_symbol.get_rect(center=((note_xloc - 3)*Staff.x_percent, (Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height)*Staff.NOTE_SIZE-1)*Staff.y_percent))
                #win.blit(flat_symbol, flat_symbol_rect)
            if note.accidental > 0:
                win.blit(Staff.sharp_img,
                 (int((note_xloc-4.5)*Staff.x_percent),
                  int((Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height+1.8)*Staff.NOTE_SIZE)*Staff.y_percent)))
                #sharp_symbol = Staff.accidental_font.render("#", True, note.note_color)
                #sharp_symbol_rect = sharp_symbol.get_rect(center=((note_xloc - 3)*Staff.x_percent, (Staff.TREBLE_MIDDLE_C_YLOC-(note.note_height)*Staff.NOTE_SIZE-0.5)*Staff.y_percent))
                #win.blit(sharp_symbol, sharp_symbol_rect)

    def render_symbol(self):
        if self.symbol_alpha > 0:
            if self.symbol_correct:
                symbol = Staff.symbol_font.render("O", True, GREEN)
            if not self.symbol_correct:
                symbol = Staff.symbol_font.render("X", True, RED)
            symbol.set_alpha(self.symbol_alpha)
            symbol_rect = symbol.get_rect(center=(int((Staff.GOAL_XLOC-0.8)*Staff.x_percent), int((Staff.TREBLE_MIDDLE_C_YLOC - Staff.NOTE_SIZE*14.9)*Staff.y_percent)))
            win.blit(symbol, symbol_rect)
            self.symbol_alpha -= self.symbol_speed

    def check_note_press(self, key):
        if (key == self.note_list[0].note_value):
            self.note_correct()
        else:
            self.note_incorrect()

    def note_correct(self):
        # MIDI notes:
        # status:   144 on, 128 off
        # data1:    note (67 = G, range: 21-108)
        # data2:    volume
        # data3:    
        self.note_list.pop(0)
        self.note_list.append(Note(self.use_accidentals))
        if self.position*Staff.x_percent < Staff.winx:
            self.position += self.note_spacing
        self.symbol_alpha = 255
        self.symbol_correct = True

    def note_incorrect(self):
        self.symbol_alpha = 255
        self.symbol_correct = False


    
class Note():

    BLACK_KEY_MODS = [1, 3, 6, 8, 10]
    NOTE_LETTERS = ["C", "D", "E", "F", "G", "A", "B"]

    def __init__(self, accidentals):
        self.note_value = 0
        self.accidental = 0
        self.note_height = 0
        self.stem_up = True
        self.accidentals = accidentals
        self.note_letter = ""
        self.note_color = BLUE
        self.generate_note_value()
        self.generate_note_height()
        self.generate_note_letter()
    
    def generate_note_value(self):
        self.note_value = random.randint(64,79)
        #self.note_value = random.choice([60,81])
        if self.accidentals == True:
            if self.note_value % 12 in Note.BLACK_KEY_MODS:
                self.accidental = random.choice([-1,1])
        else:
            while self.note_value % 12 in Note.BLACK_KEY_MODS:
                self.note_value = random.randint(64,79)
    
    def generate_note_height(self):
        # Distance on staff from Middle C (60)
        black_keys_subtracted = len([i for i in Note.BLACK_KEY_MODS if i <= self.note_value%12])
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
        self.note_letter = Note.NOTE_LETTERS[self.note_height % 7] + accidental_letter
        



def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in [3]:
    #for i in range(pygame.midi.get_count()):
        print(pygame.midi.get_default_input_id)
        print(pygame.midi.get_device_info(i), i)
        return

        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )






# -------------------------- MAIN -------------------------- 

def main():

    print_device_info()

    # Initialize MIDI
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post
    pygame.midi.init()
    
    device_id = None
    _print_device_info()
    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id
    print("using input_id :%s:" % input_id)
    input_id = 3
    
    piano_input = pygame.midi.Input(input_id)
    



    # Timer for frame rate
    frame_count = 0
    start = time.time()

    game = Staff()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                del piano_input
                pygame.midi.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    del piano_input
                    pygame.midi.quit()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    game.note_correct()
                elif event.key == pygame.K_1:
                    game.BPM += 30
                    if game.BPM > 300:
                        game.BPM = 60
                elif event.key == pygame.K_2:
                    game.note_spacing += 2
                    if game.note_spacing > 18:
                        game.note_spacing = 6
                    game.add_notes()
                elif event.key == pygame.K_3:
                    if game.staves == "Treble":
                        game.staves = "Bass"
                    elif game.staves == "Bass":
                        game.staves = "Both"
                    else:
                        game.staves = "Treble"
                elif event.key == pygame.K_4:
                    game.use_accidentals = not(game.use_accidentals)
                elif event.key == pygame.K_5:
                    game.show_letter = not(game.show_letter)
                elif event.key == pygame.K_6:
                    if game.note_type == "Whole":
                        game.note_type = "Quarter"
                    elif game.note_type == "Quarter":
                        game.note_type = "Half"
                    else:
                        game.note_type = "Whole"
                else:
                    game.note_incorrect()
            if event.type == pygame.midi.MIDIIN:
                #print(event)
                if event.status == 144:
                    print(f"TARGET: {game.note_list[0].note_value}\tPRESSED: {event.data1}")
                    game.check_note_press(event.data1)
        
        if piano_input.poll():
            midi_events = piano_input.read(10)
            # Convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, piano_input.device_id)
            for m_e in midi_evs:
                event_post(m_e)
        
        Staff.scale()
                
        game.update_note_position()
        win.fill(WHITE)
        game.render()
        pygame.display.update()

        # Calculate frame rate and update title bar with value
        frame_count += 1
        if (frame_count >= FRAMERATE):
            end = time.time()
            pygame.display.set_caption(title_bar + ' (' + str(round(frame_count/(end - start), 1)) + ' fps)')
            start = time.time()
            frame_count = 0
        fps_clock.tick(FRAMERATE)
            

main()
