'''
TODO Add PC keybindings for buttons
TODO Add error message for failed device activation
'''

from buttonclass import *

pygame.init()

class MIDIClass:

    active_device = None

    def __init__(self, win):
        self.screen = win
        self.all_devices = []
        self.input_devices = []
        self.selected_device = None
        self.refresh_progress = 100

        # x-coord, y-coord, width, height, height+spacing
        self.refresh_button = ButtonClass(self.screen, [35, 85, 30, 10, 0], "REFRESH DEVICES", c.LBLUE)
        self.no_devices_button = ButtonClass(self.screen, [10, 10, 80, 8, 12], "No input devices found", c.GREY)
        self.device_buttons = {}
        self.find_devices()
    
    def process(self):
        if self.refresh_progress < 110:
            self.refresh_progress += 10
        else:
            self.refresh_progress = 110

    def find_devices(self):
        MIDIClass.active_device = None
        self.device_buttons = {}
        pygame.midi.quit()
        pygame.midi.init()
        self.all_devices = [pygame.midi.get_device_info(i) for i in range(pygame.midi.get_count())]
        self.input_devices = [i for i,x in enumerate(self.all_devices) if x[2] == 1]  ## Change this back to:  x[2] == 1
        for i in range(len(self.input_devices)):
            print(f"DEVICE: {self.all_devices[self.input_devices[i]]}")
            self.device_buttons[self.input_devices[i]] = ButtonClass(self.screen, [10, 10, 80, 8, 12], str(self.all_devices[self.input_devices[i]][1]).split("'")[1], c.GREY, index=i)

    def activate_device(self, selection):
        MIDIClass.active_device = None
        try:
            MIDIClass.active_device = pygame.midi.Input(selection)
        except:
            print("Activation failed")
        print(f"active: {MIDIClass.active_device}")
        print()
    
    def scale(self):
        pass
    
    def render(self):
        title_text = self.screen.symbol_font.render("SELECT DEVICE:", True, c.BLACK)
        title_text_rect = title_text.get_rect(center=(int((50)*self.screen.x_percent), int((4)*self.screen.y_percent)))
        self.screen.win.blit(title_text, title_text_rect)
        self.refresh_button.render()
        if self.refresh_progress > 100:
            if len(self.input_devices) > 0:
                for name,button in self.device_buttons.items():
                    button.render()
            else:
                self.no_devices_button.render()
        else:
            pygame.draw.rect(self.screen.win,
                             c.BLUE,
                             (int(0*self.screen.x_percent),
                             int(98*self.screen.y_percent),
                             int(self.refresh_progress*self.screen.x_percent),
                             int(2*self.screen.y_percent)))
        
    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_RETURN:
                pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for name,button in self.device_buttons.items():
                if button.check(mouse_x, mouse_y):
                    self.selected_device = name
                    self.activate_device(self.selected_device)
                    self.screen.mode = "Play"
            if self.refresh_button.check(mouse_x, mouse_y):
                self.refresh_progress = 0
                self.find_devices()