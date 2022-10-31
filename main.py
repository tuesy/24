"""
24, the math card game

Rules
* draw 4 cards from 2-9 and Ace
* cards can be one of 4 suits
* can't have a card repeat
* lefty-friendly: press A or X to draw 4 more cards and B or Y to reset the game
"""
from random import choice
from time import sleep
from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332, rotate=0)
display.set_backlight(0.5)
display.set_font("bitmap8")
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)
led = RGBLED(6, 7, 8)

WIDTH, HEIGHT = display.get_bounds()
RED = display.create_pen(255, 0, 0)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
# location within the 128x128 pixel spritesheet
SPRITES = {
    "h": {"row": 4, "column": 0},
    "s": {"row": 1, "column": 11},
    "c": {"row": 8, "column": 6},
    "d": {"row": 2, "column": 1}
    }
SCALES = {"text": 8, "sprite": 10}
OFFSETS = {"x": 45, "y": -10} # sprite relative to text
CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "A"] # Ace can be either 1 or 11
SUITS = ["d", "h", "s", "c"] # diamons, hearts, spades, and clubs
MARGINS = {"top": 30, "left": 20}
LINE_SPACING = 120
DEBUG = False

def clear():
    display.set_pen(CYAN)
    display.clear()
    display.update()

# e.g. "5c" => 5 of clubs
def generate_card():
    return choice(CARDS) + choice(SUITS)

def generate_hand():
    hand = []
    for _ in range(4): # exactly 4 cards
        while True: # no dupes
            card = generate_card()
            if card not in hand:
                break
        hand.append(card)
    if DEBUG:
        print(", ".join(hand))
    return hand

def sprite(suit,x,y):
    display.sprite(SPRITES[suit]["column"], SPRITES[suit]["row"], x, y, SCALES["sprite"])

def title():
    display.set_pen(BLACK)
    x, y = (round(WIDTH/3) - 5, 100)
    display.text("24", x, y, 240, 12)
    display.sprite(15, 9, x - 7, y - 130, 16)
    display.update()

#####

if __name__ == "__main__":
    led.set_rgb(0,0,0) # turn off the led

    display.load_spritesheet("s4m_ur4i-dingbads.rgb332")

    while True:
        clear()
        title()

        while True:
            # press any of the 4 buttons
            if button_x.read() or button_a.read():
                clear()
                hand = generate_hand()
                x = MARGINS["left"]
                y = MARGINS["top"]
                index = 0
                for card in hand:
                    index += 1
                    if card[1] == 'c' or card[1] == 's': # clubs and spades are black
                        display.set_pen(BLACK)
                    else:
                        display.set_pen(RED)
                    display.text(card[0], x, y, 240, SCALES["text"])
                    sprite(card[1], x + OFFSETS["x"], y + OFFSETS["y"])
                    y += LINE_SPACING
                    if index == 2: # start second column
                        x += round(WIDTH / 2)
                        y = MARGINS["top"]
                display.update()
            elif button_y.read() or button_b.read():
                break
            sleep(0.1)