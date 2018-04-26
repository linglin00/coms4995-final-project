import pygame
import mido
from mido import MidiFile
from mido import Message

from pygame.locals import *
from mingus.core import notes, chords
from mingus.containers import *
from os import sys
import sys
import time

OCTAVES = 5  # number of octaves to show
LOWEST = 2  # lowest octave to show
FADEOUT = 0.25  # coloration fadeout time (1 tick = 0.001)
WHITE_KEY = 0
BLACK_KEY = 1
WHITE_KEYS = [
    'C',
    'D',
    'E',
    'F',
    'G',
    'A',
    'B',
    ]
BLACK_KEYS = ['C#', 'D#', 'F#', 'G#', 'A#']

note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def convert_int_to_note(msg):
    note_name = "C"
    tnote_octave = 4
    #tnote_dynamics = {}
    if msg.note == 1:
        note_name = "A"
    elif msg.note == 2:
        note_name = "A#"
    elif msg.note == 3:
        note_name = "B"
    else:
        nrange = int((msg.note - 3) / len(note_names))
        nidx = msg.note - 4 - nrange * len(note_names)
        note_name = note_names[nidx]
        note_octave = nrange + 1
    myNote = Note(note_name, note_octave)
    myNote.velocity = msg.velocity
    myNote.channel = msg.channel
    return myNote

def load_img(name):
    """Load image and return an image object"""
    fullname = name
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except (pygame.error, message):
        print ("Error: couldn't load image: "%fullname)
        raise (SystemExit, message)
    return (image, image.get_rect())

def play_note(note):
    """play_note determines the coordinates of a note on the keyboard image
    and sends a request to play the note to the fluidsynth server"""

    global text
    octave_offset = (note.octave - LOWEST) * width
    if note.name in WHITE_KEYS:

        # Getting the x coordinate of a white key can be done automatically

        w = WHITE_KEYS.index(note.name) * white_key_width
        w = w + octave_offset

        # Add a list containing the x coordinate, the tick at the current time
        # and of course the note itself to playing_w

        playing_w.append([w, tick, note])
    else:

        # For black keys I hard coded the x coordinates. It's ugly.

        i = BLACK_KEYS.index(note.name)
        if i == 0:
            w = 18
        elif i == 1:
            w = 58
        elif i == 2:
            w = 115
        elif i == 3:
            w = 151
        else:
            w = 187
        w = w + octave_offset
        playing_b.append([w, tick, note])

    # To find out what sort of chord is being played we have to look at both the
    # white and black keys, obviously:

    notes = playing_w + playing_b
    notes.sort()
    notenames = []
    for n in notes:
        notenames.append(n[2].name)

    # Determine the chord

    det = chords.determine(notenames)
    if det != []:
        det = det[0]
    else:
        det = ''

    # And render it onto the text surface

    t = font.render(det, 2, (0, 0, 0))
    text.fill((255, 255, 255))
    text.blit(t, (0, 0))
    
## MAIN START 
filename = sys.argv[1]
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('monospace', 12)
screen = pygame.display.set_mode((640, 480))

(key_graphic, kgrect) = load_img('keys.png')
(width, height) = (kgrect.width, kgrect.height)
white_key_width = width / 7

# Reset display to wrap around the keyboard image

pygame.display.set_mode((OCTAVES * width, height + 20))
pygame.display.set_caption('mingus piano')
octave = 7
channel = 8

# pressed is a surface that is used to show where a key has been pressed

pressed = pygame.Surface((white_key_width, height))
pressed.fill((0, 230, 0))

# text is the surface displaying the determined chord

text = pygame.Surface((width * OCTAVES, 20))
text.fill((255, 255, 255))
playing_w = []  # white keys being played right now
playing_b = []  # black keys being played right now
quit = False
tick = 0.0

time.sleep(5)
port = mido.open_output()
#mid = MidiFile('01Allemande.mid')
mid = MidiFile(filename)

for msg1 in mid.play():
    #print(msg)
    msg = mido.Message.from_str(str(msg1))
    port.send(msg)
    
    # Blit the picture of one octave OCTAVES times.

    for x in range(OCTAVES):
        screen.blit(key_graphic, (x * width, 0))

    # Blit the text surface

    screen.blit(text, (0, height))

    # Check all the white keys

    for note in playing_w:
        diff = tick - note[1]

        # If a is past its prime, remove it, otherwise blit the pressed surface
        # with a 'cool' fading effect.

        #if diff > FADEOUT:
        if msg.type == 'note_off':
            playing_w.remove(note)
        else:
            pressed.fill((255, ((FADEOUT - diff) / FADEOUT) * 32, 124))
            screen.blit(pressed, (note[0], 0), None, pygame.BLEND_SUB)

    # Now check all the black keys. This redundancy could have been prevented,
    # but it isn't any less clear like this

    for note in playing_b:
        diff = tick - note[1]
        
        # Instead of SUB we ADD this time, and change the coloration

        #if diff > FADEOUT:
        if msg.type == 'note_off':
            playing_b.remove(note)
        else:
            pressed.fill((((FADEOUT - diff) / FADEOUT) * 125, 255, 125))
            screen.blit(pressed, (note[0], 1), (0, 0, 19, 68), pygame.BLEND_ADD)

    # Check for keypresses
    if msg.type == 'note_on' or msg.type == 'note_off':
        play_note(convert_int_to_note(msg))
    
        # Update the screen

        pygame.display.update()
        tick += 0.001

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()

pygame.quit()