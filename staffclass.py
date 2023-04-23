'''
TODO Relocate image loading/scaling code
TODO Standardize image sizes of accidentals
TODO Diagnose aliasing of images
'''

from noteclass import *

pygame.init()

class StaffClass:

    # User Variables
    bpm = 120
    note_spacing = 12
    use_accidentals = True
    show_note_letter = True
    show_MIDI_value = True
    note_type = "Quarter"
    ##

    staff_spacing = 36

    def __init__(self, win, staff_num):
        self.screen = win
        self.staff_num = staff_num

        self.x = 6
        self.y = 35 + self.staff_num*StaffClass.staff_spacing
        self.goal_x = 24
        self.array_x = 100
        self.note_size = 2

        # User variables
        self.highest_note = 64
        self.lowest_note = 57
        ##

        self.note_qty = int(100/StaffClass.note_spacing)
        self.notes = [NoteClass(self) for i in range(self.note_qty)]

        self.symbol_correct = False
        self.symbol_speed = 2.5  # Lower is faster
        self.symbol_timer = 0
        self.symbol_alpha = 0

        # Images
        self.clef_ratio = 323/134
        self.treble_clef_img = pygame.image.load("graphics/treble_clef.png").convert_alpha()
        self.bass_clef_img = pygame.image.load("graphics/bass_clef.png").convert_alpha()
        self.sharp_ratio = 142/45
        self.sharp_img = pygame.image.load("graphics/sharp.png").convert_alpha()
        self.flat_ratio = 142/45
        self.flat_img = pygame.image.load("graphics/flat.png").convert_alpha()
        self.note_ratio = 188/80
        self.whole_note_img = pygame.image.load("graphics/whole_note.png").convert_alpha()
        self.half_note_up_img = pygame.image.load("graphics/half_note.png").convert_alpha()
        self.half_note_down_img = pygame.transform.rotate(pygame.image.load("graphics/half_note.png").convert_alpha(),180)
        self.quarter_note_up_img = pygame.image.load("graphics/quarter_note.png").convert_alpha()
        self.quarter_note_down_img = pygame.transform.rotate(pygame.image.load("graphics/quarter_note.png").convert_alpha(),180)
        
        self.treble_clef_img = pygame.transform.scale(self.treble_clef_img, (int(13*self.screen.y_percent),int(13*self.screen.y_percent*self.clef_ratio)))
        self.bass_clef_img = pygame.transform.scale(self.bass_clef_img, (int(13*self.screen.y_percent),int(13*self.screen.y_percent*self.clef_ratio)))
        self.sharp_img = pygame.transform.scale(self.sharp_img, (int(2.5*self.screen.y_percent),int(2.5*self.screen.y_percent*self.sharp_ratio)))
        self.flat_img = pygame.transform.scale(self.flat_img, (int(3*self.screen.y_percent),int(3*self.screen.y_percent*self.flat_ratio)))
        self.whole_note_img = pygame.transform.scale(self.whole_note_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        self.half_note_up_img = pygame.transform.scale(self.half_note_up_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        self.half_note_down_img = pygame.transform.scale(self.half_note_down_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        self.quarter_note_up_img = pygame.transform.scale(self.quarter_note_up_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        self.quarter_note_down_img = pygame.transform.scale(self.quarter_note_down_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        ##
    
    def process(self):
        self.update_array_position()
    
    def change_accidentals(self):
        if StaffClass.use_accidentals == True:
            for note in self.notes:
                note.add_accidental()
        else:
            for note in self.notes:
                note.remove_accidental()

    def add_notes(self):
        self.note_qty = int(100/StaffClass.note_spacing)
        if len(self.notes) < self.note_qty:
            for i in range(self.note_qty):
                self.notes.append(NoteClass(self))
        elif len(self.notes) > self.note_qty:
            self.notes = self.notes[0:self.note_qty]
    
    def update_array_position(self):
        self.array_x = max(self.array_x - (StaffClass.note_spacing/c.FRAMERATE*(StaffClass.bpm/c.FRAMERATE)), self.goal_x)
        for note_index, note in enumerate(self.notes):
            note.update_note_positions(note_index)

    def scale(self):
        self.treble_clef_img = pygame.image.load("graphics/treble_clef.png").convert_alpha()
        self.bass_clef_img = pygame.image.load("graphics/bass_clef.png").convert_alpha()
        self.sharp_img = pygame.image.load("graphics/sharp.png").convert_alpha()
        self.flat_img = pygame.image.load("graphics/flat.png").convert_alpha()
        self.whole_note_img = pygame.image.load("graphics/whole_note.png").convert_alpha()
        self.half_note_up_img = pygame.image.load("graphics/half_note.png").convert_alpha()
        self.half_note_down_img = pygame.transform.rotate(pygame.image.load("graphics/half_note.png").convert_alpha(),180)
        self.quarter_note_up_img = pygame.image.load("graphics/quarter_note.png").convert_alpha()
        self.quarter_note_down_img = pygame.transform.rotate(pygame.image.load("graphics/quarter_note.png").convert_alpha(),180)
        self.treble_clef_img = pygame.transform.scale(self.treble_clef_img, (int(13*self.screen.y_percent),int(13*self.screen.y_percent*self.clef_ratio)))
        self.bass_clef_img = pygame.transform.scale(self.bass_clef_img, (int(13*self.screen.y_percent),int(13*self.screen.y_percent*self.clef_ratio)))
        self.sharp_img = pygame.transform.scale(self.sharp_img, (int(2.5*self.screen.y_percent),int(2.5*self.screen.y_percent*self.sharp_ratio)))
        self.flat_img = pygame.transform.scale(self.flat_img, (int(3*self.screen.y_percent),int(3*self.screen.y_percent*self.flat_ratio)))
        self.whole_note_img = pygame.transform.scale(self.whole_note_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        self.half_note_up_img = pygame.transform.scale(self.half_note_up_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        self.half_note_down_img = pygame.transform.scale(self.half_note_down_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        self.quarter_note_up_img = pygame.transform.scale(self.quarter_note_up_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        self.quarter_note_down_img = pygame.transform.scale(self.quarter_note_down_img, (int(7*self.screen.y_percent),int(7*self.screen.y_percent*self.note_ratio)))
        for note in self.notes:
            note.scale()
    
    def render(self):
        # Ledger lines
        for i in range(5):
            pygame.draw.rect(self.screen.win,
                             c.BLACK,
                             (int(self.x*self.screen.x_percent),
                              int((self.y-(i+1)*self.note_size*2)*self.screen.y_percent),
                              int((100)*self.screen.x_percent),
                              2))
        # Clef
        clef_choice = self.treble_clef_img if self.staff_num == 0 else self.bass_clef_img
        self.screen.win.blit(clef_choice,
            (int((self.x+2)*self.screen.x_percent),
            int((self.y-28)*self.screen.y_percent)))
        # Goal Lines
        pygame.draw.rect(self.screen.win,
                         c.BLACK,
                         (int((self.x+13)*self.screen.x_percent),
                          int((self.y-self.note_size*10)*self.screen.y_percent),
                          2,
                          int((self.note_size*8)*self.screen.y_percent)))
        for note in self.notes:
            # Note Value
            if StaffClass.show_MIDI_value == True:
                MIDI_num = self.screen.basic_font.render(str(note.note_value), True, c.BLUE)
                MIDI_num_rect = MIDI_num.get_rect(center=(int((note.x + self.note_size)*self.screen.x_percent), int((self.y - 31)*self.screen.y_percent)))
                self.screen.win.blit(MIDI_num, MIDI_num_rect)
            # Note Letter
            if StaffClass.show_note_letter == True:
                note_letter = self.screen.basic_font.render(str(note.note_letter), True, c.BLUE)
                note_letter_rect = note_letter.get_rect(center=(int((note.x + self.note_size)*self.screen.x_percent), int((self.y - 28)*self.screen.y_percent)))
                self.screen.win.blit(note_letter, note_letter_rect)
            # Ledger Lines
            if note.note_value >= 50:
                if note.note_height < 1:
                    for ledgerLine in range((2-note.note_height)//2):
                        pygame.draw.rect(self.screen.win,
                                         c.BLACK,
                                         (int((note.x)*self.screen.x_percent),
                                          int((self.y+(ledgerLine*2)*self.note_size)*self.screen.y_percent),
                                          int((self.note_size*2)*self.screen.x_percent),
                                          2))
                if note.note_height > 11:
                    for ledgerLine in range((note.note_height-10)//2):
                        pygame.draw.rect(self.screen.win,
                                         c.BLACK,
                                         (int((note.x)*self.screen.x_percent),
                                          int((self.y-(12*self.note_size)-(ledgerLine*2)*self.note_size)*self.screen.y_percent),
                                          int((self.note_size*2)*self.screen.x_percent),
                                          2))
           
            note.render(StaffClass.note_type)
            self.render_response_symbol()
    
    def render_response_symbol(self):
        if self.symbol_alpha > 0:
            if self.symbol_correct:
                symbol = self.screen.symbol_font.render("O", True, c.GREEN)
            if not self.symbol_correct:
                symbol = self.screen.symbol_font.render("X", True, c.RED)
            symbol.set_alpha(self.symbol_alpha)
            symbol_rect = symbol.get_rect(center=(int((self.x + 13)*self.screen.x_percent), int((self.y - 28)*self.screen.y_percent)))
            self.screen.win.blit(symbol, symbol_rect)
            self.symbol_alpha -= self.symbol_speed
    
    def check_note_press(self, key):
        if (key == self.notes[0].note_value):
            self.note_correct()
        else:
            self.note_incorrect()
    
    def note_correct(self):
        # MIDI notes:
        # status:   144 on, 128 off
        # data1:    note (67 = G, range: 21-108)
        # data2:    volume
        # data3:    
        self.notes.pop(0)
        self.notes.append(NoteClass(self))
        if self.array_x*self.x < self.screen.x:
            self.array_x += StaffClass.note_spacing
        self.symbol_alpha = 255
        self.symbol_correct = True

    def note_incorrect(self):
        self.symbol_alpha = 255
        self.symbol_correct = False
        
    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.note_correct()
            else:
                self.note_incorrect()
        if event.type == pygame.midi.MIDIIN:
            #print(event)
            if event.status == 144:
                print(f"TARGET: {self.notes[0].note_value}\tPRESSED: {event.data1}")
                self.check_note_press(event.data1)
        for note in self.notes:
            note.process_events(event)