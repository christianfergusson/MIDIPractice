'''
TODO Add Staves option
TODO Add Range option
TODO Add PC keybinding labels for buttons
TODO Add piano keybindings for buttons (low notes)
'''

from staffclass import *
from midiclass import *

pygame.init()

class WinClass:

    basic_font = pygame.font.SysFont('Calibri', 18)
    symbol_font = pygame.font.SysFont('Calibri', 36, bold=True)

    def __init__(self, win_x, win_y):
        MONITOR_RESOLUTION = pygame.display.Info()
        MONITOR_X = MONITOR_RESOLUTION.current_w
        MONITOR_Y = MONITOR_RESOLUTION.current_h
        self.x = min(win_x, MONITOR_X*0.9)
        self.y = min(win_y, MONITOR_Y*0.9)
        self.x_percent = self.x/100
        self.y_percent = self.y/100
        self.win = pygame.display.set_mode((self.x, self.y), pygame.RESIZABLE)
        pygame.display.set_caption("Sight Reading Practice")

        self.mode = "Select Device"

        self.device = MIDIClass(self)

        self.staff_qty = 1
        self.staves = [StaffClass(self, i) for i in range(self.staff_qty)]

        button_buffer = 3.5
        button_top_y = 80
        button_bot_y = 90
        button_w = 18
        button_h = 8
        button_space = button_w + 1
        self.buttons = {"BPM": ButtonClass(self, [button_buffer+0*button_space, button_top_y, button_w, button_h, 0], f"BPM: {StaffClass.bpm}", c.LBLUE),
                        "Note Spacing": ButtonClass(self, [button_buffer+0*button_space, button_bot_y, button_w, button_h, 0], f"Spacing: {StaffClass.note_spacing}", c.LBLUE),
                        "Staves": ButtonClass(self, [button_buffer+1*button_space, button_top_y, button_w, button_h, 0], f"Staves: #####", c.LBLUE),
                        "Range": ButtonClass(self, [button_buffer+1*button_space, button_bot_y, button_w, button_h, 0], f"Range: #####", c.LBLUE),
                        "Use Accidentals": ButtonClass(self, [button_buffer+2*button_space, button_top_y, button_w, button_h, 0], f"Accidentals: {StaffClass.use_accidentals}", c.LBLUE),
                        "Note Type": ButtonClass(self, [button_buffer+2*button_space, button_bot_y, button_w, button_h, 0], f"Note Type: {StaffClass.note_type}", c.LBLUE),
                        "Show Note Letter": ButtonClass(self, [button_buffer+3*button_space, button_top_y, button_w, button_h, 0], f"Note Letter: {StaffClass.show_note_letter}", c.LBLUE),
                        "Show MIDI Value": ButtonClass(self, [button_buffer+3*button_space, button_bot_y, button_w, button_h, 0], f"MIDI Value: {StaffClass.show_MIDI_value}", c.GREY),
                        "Change Device": ButtonClass(self, [button_buffer+4*button_space, button_bot_y, button_w, button_h, 0], "Change Device", c.RED)}
    
    def process(self):
        if self.mode == "Play":
            for staff in self.staves:
                staff.process()
        elif self.mode == "Select Device":
            self.device.process()
    
    def scale(self):
        self.x, self.y = self.win.get_size()
        self.x_percent = self.x/100
        self.y_percent = self.y/100
        WinClass.basic_font = pygame.font.SysFont('Calibri', int(self.y/33))
        WinClass.symbol_font = pygame.font.SysFont('Calibri', int(self.y/15), bold=True)
        if self.mode == "Play":
            for staff in self.staves:
                staff.scale()
        elif self.mode == "Select Device":
            self.device.scale()
    
    def render(self):
        if self.mode == "Play":
            for staff in self.staves:
                staff.render()
            for name, button in self.buttons.items():
                button.render()
        elif self.mode == "Select Device":
            self.device.render()
    
    def clear(self):
        self.win.fill(c.WHITE)

    def event_change_device(self):
        self.mode = "Select Device"
        self.device.find_devices()
    
    def event_BPM(self):
        StaffClass.bpm += 30
        if StaffClass.bpm > 300:
            StaffClass.bpm = 60
        self.buttons["BPM"].text = f"BPM: {StaffClass.bpm}"
    
    def event_note_spacing(self):
        StaffClass.note_spacing += 2
        if StaffClass.note_spacing > 18:
            StaffClass.note_spacing = 6
        for staff in self.staves:
            staff.add_notes()
        self.buttons["Note Spacing"].text = f"Spacing: {StaffClass.note_spacing}"
    
    def event_staves(self):
        self.buttons["Staves"].text = f"Staves: #####"
    
    def event_range(self):
        self.buttons["Range"].text = f"Range: #####"
    
    def event_use_accidentals(self):
        StaffClass.use_accidentals = not(StaffClass.use_accidentals)
        self.buttons["Use Accidentals"].text = f"Accidentals: {StaffClass.use_accidentals}"
        for staff in self.staves:
            staff.change_accidentals()
    
    def event_note_type(self):
        if StaffClass.note_type == "Whole":
            StaffClass.note_type = "Quarter"
        elif StaffClass.note_type == "Quarter":
            StaffClass.note_type = "Half"
        else:
            StaffClass.note_type = "Whole"
        self.buttons["Note Type"].text = f"Note Type: {StaffClass.note_type}"
    
    def event_show_note_letter(self):
        StaffClass.show_note_letter = not(StaffClass.show_note_letter)
        self.buttons["Show Note Letter"].text = f"Note Letter: {StaffClass.show_note_letter}"
    
    def event_show_MIDI_value(self):
        StaffClass.show_MIDI_value = not(StaffClass.show_MIDI_value)
        self.buttons["Show MIDI Value"].text = f"MIDI Value: {StaffClass.show_MIDI_value}"
        
    def process_events(self, event):
        if event.type == pygame.VIDEORESIZE:
            if event.w < event.h*1.3:
                self.win = pygame.display.set_mode((event.h*1.3, event.h), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_1:
                self.event_BPM()
            elif event.key == pygame.K_2:
                self.event_note_spacing()
            elif event.key == pygame.K_3:
                self.event_staves()
            elif event.key == pygame.K_4:
                self.event_range()
            elif event.key == pygame.K_5:
                self.event_use_accidentals()
            elif event.key == pygame.K_6:
                self.event_note_type()
            elif event.key == pygame.K_7:
                self.event_show_note_letter()
            elif event.key == pygame.K_8:
                self.event_show_MIDI_value()
            elif event.key == pygame.K_9:
                self.event_change_device()
        if self.mode == "Play":
            for staff in self.staves:
                staff.process_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.buttons["Change Device"].check(mouse_x, mouse_y):
                    self.event_change_device()
                elif self.buttons["BPM"].check(mouse_x, mouse_y):
                    self.event_BPM()
                elif self.buttons["Note Spacing"].check(mouse_x, mouse_y):
                    self.event_note_spacing()
                elif self.buttons["Staves"].check(mouse_x, mouse_y):
                    self.event_staves()
                elif self.buttons["Range"].check(mouse_x, mouse_y):
                    self.event_range()
                elif self.buttons["Use Accidentals"].check(mouse_x, mouse_y):
                    self.event_use_accidentals()
                elif self.buttons["Note Type"].check(mouse_x, mouse_y):
                    self.event_note_type()
                elif self.buttons["Show Note Letter"].check(mouse_x, mouse_y):
                    self.event_show_note_letter()
                elif self.buttons["Show MIDI Value"].check(mouse_x, mouse_y):
                    self.event_show_MIDI_value()
        elif self.mode == "Select Device":
            self.device.process_events(event)