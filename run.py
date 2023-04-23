'''
TODO
'''

import sys

from pygame import midi
from pygame.locals import *

from winclass import *


pygame.init()
screen = WinClass(800, 600)
fps_clock = pygame.time.Clock()


def exit():
    del MIDIClass.active_device
    pygame.midi.quit()
    pygame.quit()
    sys.exit()

def main_process_events(event):
    if event.type == QUIT:
        exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            exit()

def main():

    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post
    pygame.midi.init()

    ## Move this to midiclass?
    piano = None

    while True:
        
        for event in pygame.event.get():
            main_process_events(event)
            screen.process_events(event)
        
        ## Move this to midiclass?
        if MIDIClass.active_device != None:
            if MIDIClass.active_device.poll():
                midi_events = MIDIClass.active_device.read(10)
                # Convert them into pygame events.
                midi_evs = pygame.midi.midis2events(midi_events, MIDIClass.active_device.device_id)
                for m_e in midi_evs:
                    event_post(m_e)

        screen.scale()
        screen.process()
        screen.clear()
        screen.render()
        pygame.display.update()

        fps_clock.tick(c.FRAMERATE)

main()