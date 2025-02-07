# "import asyncio" import here?
import os
import math
import pygame
import sys
import random
from pygame.locals import *
from moviepy.editor import VideoFileClip # vid import stuff

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)
# Initialize Pygame
pygame.init()
pygame.mixer.init()

current_volume = 0.5
pygame.mixer.music.set_volume(current_volume)
# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
GRID_SIZE = 3
CARD_WIDTH = 160
CARD_HEIGHT = 235
BOARD_ORIGIN_X = (WINDOW_WIDTH - (GRID_SIZE * CARD_WIDTH)) // 2
BOARD_ORIGIN_Y = (WINDOW_HEIGHT - (GRID_SIZE * CARD_HEIGHT)) // 2
FPS = 30

# music btn rects v
#play & other btn imgs v
play_image = pygame.image.load('images/icons/play_btn.png')
play_image = pygame.transform.scale(play_image, (50, 50))
pause_image = pygame.image.load('images/icons/pause_btn.png')
pause_image = pygame.transform.scale(pause_image, (50, 50))
vol_up_img = pygame.image.load('images/icons/vol_up.png')
vol_up_img = pygame.transform.scale(vol_up_img, (50, 50))
vol_dn_img = pygame.image.load('images/icons/vol_dn.png')
vol_dn_img = pygame.transform.scale(vol_dn_img, (50, 50))
#play & other btn imgs ^

pause_button_rect = pygame.Rect(50, 50, 50, 50)  # Example for pause button
play_button_rect = pygame.Rect(120, 50, 50, 50)  # Example for play button
volume_up_rect = pygame.Rect(200, 50, 50, 50)    # Example for volume up button
volume_down_rect = pygame.Rect(280, 50, 50, 50)
# music btn rects ^

# Colors
TYPE_ON_CARDS = (247, 220, 210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# RED = (255, 0, 0)
RED = (172, 19, 45) # pygame will accept HEX code for colors but this creates issue for color change animation function
YELLOW = (255, 255, 0)
BLUE = (19, 114, 172)
GREY = (200, 200, 200)
GREEN = (42, 197, 81)
BRIGHTGREEN = (0, 255, 0)

# music v
pygame.mixer.music.load('music/9convert.com - Hades II The Silver Sisters.ogg')  # Adjust to your file path
pygame.mixer.music.play(-1)  # Loop indefinitely
pygame.mixer.music.set_volume(0.5)

# sounds
card_flip_sound = pygame.mixer.Sound('music/soundFX/card_color_change_sound.ogg')
selection_is_made_sound = pygame.mixer.Sound('music/soundFX/select_something.ogg')
new_game_sound = pygame.mixer.Sound('music/soundFX/new_game.ogg')
# sounds
# music ^

# Set up display
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Vionarch')
FPS_CLOCK = pygame.time.Clock()

# image import v
BORDER_IMAGE_PATH = "images/card/card_boarder_image.png"  # Replace with the path to your image file
BACKGROUND_forBoard_IMG_PATH = "images/backgrounds/depositphotos_1750670-stock-photo-zodiac-disc-gold.jpg" # path to bg
BACKGROUND_forTitle_and_GO_PATH = 'images/backgrounds/wheel-zodiac-signs-14292638.webp'
BACK_OF_A_CARD_path = 'images/card/back_of_card.jpg'

BOCard_Image = pygame.image.load(BACK_OF_A_CARD_path)
BOCard_Image = pygame.transform.scale(BOCard_Image, (CARD_WIDTH, CARD_HEIGHT))

BORDER_IMAGE = pygame.image.load(BORDER_IMAGE_PATH)
BORDER_IMAGE = pygame.transform.scale(BORDER_IMAGE, (CARD_WIDTH + 7, CARD_HEIGHT + 7))  # Adjust the size if necessary

BG_baord_IMAGE = pygame.image.load(BACKGROUND_forBoard_IMG_PATH) # loads in bg
BG_board_IMAGE = pygame.transform.scale(BG_baord_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT)) # scales bg to display size

BG_Title_GO_IMAGE = pygame.image.load(BACKGROUND_forTitle_and_GO_PATH)
BG_Title_GO_IMAGE = pygame.transform.scale(BG_Title_GO_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
# image import ^

# Define the selection modes
DECK_SELECTION = 0
GRID_SELECTION = 1

# Start in deck selection mode
selection_mode = DECK_SELECTION

selected_card_index = 0
grid_row, grid_col = 0, 0

# AI team vars
player_team = None
ai_team = None



def fade_out(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill(BLACK)
    for alpha in range(0, 175):
        fade.set_alpha(alpha)
        # show_title_screen() # may need to change
        DISPLAYSURF.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)
        
    
def fade_in(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill(BLACK)
    for alpha in range(174, -1, -1):  # Start from 174 down to 0
        fade.set_alpha(alpha)
        DISPLAYSURF.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)
        
# video function v


# new cards stuff v

TOTAL_CARDS = [
    ([1, 2, 3, 4], "Cat", "Just a fuckin cat"),
    ([7, 4, 5, 4], "Lestolen", "Lion Hunter prince of the Zoraznor plaines"),
    ([5, 5, 5, 5], "Deer", "a damn deer"),
    ([6, 6, 6, 6], "Pig", "will be bacon soon"),
    ([2, 3, 4, 5], "Dog", "Is a good boy"),
    ([5, 4, 3, 2], "Monkey", "eats bananas"), 
    ([7, 7, 7, 7], "Water Kapa", "using water as its body, i can walk upright"), 
    ([8, 8, 8, 8], "Giraffe", "has a long neck"),
    ([3, 4, 5, 6], "Horse", "just a goddamn horse"), 
    ([6, 5, 4, 3], "Duck", "Quaks and shit"), 
    ([9, 9, 9, 9], "Camel", "has a hump, lives in the dessert"), 
    ([1, 1, 1, 1],"Heron", "lives in rivers and is tall"),
    ([2, 2, 2, 2], "Bull", "Has horns and is angry"), 
    ([3, 3, 3, 3], "Sir Guir", "knight on horseback.. looks cool"), 
    ([6, 5, 8, 8], "Hecterra", "bearer of the acuresd visage"), 
    ([5, 5, 5, 5], "Koala", "is cute"),
    ([6, 6, 6, 6], "Leopard", "Death with spots on it"), 
    ([7, 7, 8, 7], "Lion", "Had better watch out for lestolon"), 
    ([8, 8, 8, 8], "Bird", "silly ass bird"), 
    ([9, 9, 7, 9], "Raven", "More serious bird"),
    ([1, 2, 3, 4], "Sea Turtle", "swimmy turtle boi"), 
    ([4, 3, 2, 1], "Shark", "Doesnt bite as often as you'd think"), 
    ([5, 6, 7, 8], "Squid", "shoots ink at ya"), 
    ([8, 7, 6, 5], "Tortoise", "is this dogge?"),
    ([1, 1, 1, 9], "Fukt Up", "place holder illustration"), 
    ([9, 1, 1, 1], "Wolf's head", "crest of house durren"), 
    ([2, 2, 2, 8], "Blue Goo", "Species of water kapa with a habit of drowning tressure seekers"), 
    ([8, 4, 6, 7], "Red Hood", "Devout ssurvant of the crimson flame"),
    ([3, 3, 3, 7], "wolf", "spicy doggo"), 
    ([7, 3, 3, 3], "Green bat", "Emits a piercing scream")
]

# Load images
def load_images():
    image_dict = {
        1: pygame.image.load('images/card/cat.png'),
        2: pygame.image.load('images/card/Lion_hunter.png'),
        3: pygame.image.load('images/card/deer.png'),
        4: pygame.image.load('images/card/314293.png'),
        5: pygame.image.load('images/card/dog.png'),
        6: pygame.image.load('images/card/animal-monkey-silhouette-png.png'),
        7: pygame.image.load('images/card/IMG_0945.png'),
        8: pygame.image.load('images/card/girrafe.png'),
        9: pygame.image.load('images/card/33774.png'),
        10: pygame.image.load('images/card/duck.webp'),
        11: pygame.image.load('images/card/camel.png'),
        12: pygame.image.load('images/card/heron.png'),
        13: pygame.image.load('images/card/bull.png'),
        14: pygame.image.load('images/card/knight_on_horse.png'),
        15: pygame.image.load('images/card/Hecterra.png'),
        16: pygame.image.load('images/card/koala.png'),
        17: pygame.image.load('images/card/leopard.png'),
        18: pygame.image.load('images/card/lion.png'),
        19: pygame.image.load('images/card/simple-bird-flying-silhouette-08e636.webp'),
        20: pygame.image.load('images/card/raven.png'),
        21: pygame.image.load('images/card/sea turtle.png'),
        22: pygame.image.load('images/card/shark.png'),
        23: pygame.image.load('images/card/squid.png'),
        24: pygame.image.load('images/card/tortoise.png'),
        25: pygame.image.load('images/card/IMG_0949.png'),
        26: pygame.image.load('images/card/wolf_head.png'),
        27: pygame.image.load('images/card/IMG_0946.png'),
        28: pygame.image.load('images/card/red_cultist.png'),
        29: pygame.image.load('images/card/wolf.png'),
        30: pygame.image.load('images/card/green_bat.png')
        # Add paths for all necessary images
    }
    for key in image_dict:
        image_dict[key] = pygame.transform.scale(image_dict[key], (CARD_WIDTH, CARD_HEIGHT))
    return image_dict

images = load_images()


class Card:
    def __init__(self, team, sides, image, name, statement):
        self.team = team
        self.sides = sides  # top, bottom, left, right
        self.color = RED if team == 'red' else BLUE
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        self.border_image = BORDER_IMAGE
        self.image = image
        self.name = name
        self.statement = statement

    def draw(self, surface):
        # this basically draws things on the surface of the cards
        # Draw border image
        border_rect = self.border_image.get_rect(topleft=(self.rect.x - 3, self.rect.y - 3))  # Adjust offset to center the border
        surface.blit(self.border_image, border_rect)

        # Draw card
        pygame.draw.rect(surface, self.color, self.rect)

        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)

        font = pygame.font.Font('fonts/old_celtiberian/Old Celtiberians.otf', 25) # was None
        nums = [(self.rect.x + CARD_WIDTH // 2, self.rect.y + 9),
                (self.rect.x + CARD_WIDTH // 2, self.rect.y + CARD_HEIGHT - 10),
                (self.rect.x + 5, self.rect.y + CARD_HEIGHT // 2),
                (self.rect.x + CARD_WIDTH - 25, self.rect.y + CARD_HEIGHT // 2)]
        for num, pos in zip(self.sides, nums):
            text = font.render(str(num), True, TYPE_ON_CARDS)
            text_rect = text.get_rect(center=pos)
            surface.blit(text, text_rect)

        # Draw card name in the top-right corner of the card
        name_font = pygame.font.Font('fonts/adon/Adon Black.otf', 12) # Small font for card name
        name_text = name_font.render(self.name, True, (TYPE_ON_CARDS))  # White text
        name_rect = name_text.get_rect(topright=(self.rect.right - 5, self.rect.top + 15))  # Top-right corner
        surface.blit(name_text, name_rect)

    def animate_color_change(self, new_team):
        # Store the current color (before change) and determine the new color (based on team)
        old_color = self.color  # The current color of the card (either red or blue)
        new_color = RED if new_team == 'red' else BLUE  # Set the new color depending on the new team

        # Play the card flip sound with a set volume
        card_flip_sound.set_volume(0.4)  # Set the volume of the sound to 40% of the maximum
        card_flip_sound.play()  # Play the flip sound to accompany the visual change

        # Animation loop: gradually blend from the old color to the new color over 16 steps
        for i in range(16):  # 16 frames for the animation (you can adjust this number for speed)
            ratio = i / 23  # Ratio determines how far along the animation is (0 at start, 1 at end)

            # Interpolate (blend) between the old color and the new color based on the ratio
            # The ratio gradually goes from 0 to 1, transitioning from old_color to new_color
            self.color = (
                int(old_color[0] * (1 - ratio) + new_color[0] * ratio),  # Red component
                int(old_color[1] * (1 - ratio) + new_color[1] * ratio),  # Green component
                int(old_color[2] * (1 - ratio) + new_color[2] * ratio)   # Blue component
            )

            # Redraw the board and update the display
            # 'draw_board()' function will redraw the game state (with updated card colors)
            draw_board()  # Draw the game board and cards (with the updated card's current color)
            pygame.display.update()  # Update the display to show the new frame of the animation

            # Control the frame rate to ensure the animation runs at the desired FPS
            FPS_CLOCK.tick(FPS)  # Wait so that the next frame occurs at the correct speed (FPS frames per second)

        # After the animation completes, update the card's team and final color
        self.team = new_team  # Set the card's team to the new team (so it now "belongs" to the other side)
        self.color = new_color  # Set the card's color to the final new color (either red or blue)


# Initialize board

#zigzag start
def initialize_board():
    global board, red_cards, blue_cards, dragging_card, current_team, player_team

    # Create and shuffle indices for random selection
    indices = list(range(len(TOTAL_CARDS)))
    random.shuffle(indices)

    # Use shuffled indices to get random cards for each team
    red_indices = indices[:5]
    blue_indices = indices[5:10]

    # Assign cards using the shuffled indices
    red_cards = [
        Card('red', TOTAL_CARDS[idx][0], images[idx + 1], TOTAL_CARDS[idx][1], TOTAL_CARDS[idx][2]) 
        for idx in red_indices
    ]
    blue_cards = [
        Card('blue', TOTAL_CARDS[idx][0], images[idx + 1], TOTAL_CARDS[idx][1], TOTAL_CARDS[idx][2]) 
        for idx in blue_indices
    ]

    # Initialize an empty board
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Positioning code for red cards (e.g., zigzag pattern)
    for i, card in enumerate(red_cards):
        x_offset = -CARD_WIDTH * 1.5 + (i % 2) * -60  # Adjust x offset to create zigzag
        y_offset = BOARD_ORIGIN_Y + i * (CARD_HEIGHT // 2) * 1.1
        card.rect.topleft = (BOARD_ORIGIN_X + x_offset, y_offset)

    # Positioning code for blue cards (e.g., zigzag pattern)
    for i, card in enumerate(blue_cards):
        x_offset = GRID_SIZE * CARD_WIDTH + CARD_WIDTH // 2 + (i % 2) * 60  # Adjust x offset to create zigzag
        y_offset = BOARD_ORIGIN_Y + i * (CARD_HEIGHT // 2) * 1.1
        card.rect.topleft = (BOARD_ORIGIN_X + x_offset, y_offset)

    # Initialize game state variables
    dragging_card = None
    current_team = random.choice(['red', 'blue'])
    player_team = None

#zig zag end

initialize_board()

# Function to draw the grid
def draw_grid():
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(DISPLAYSURF, BLACK, 
                         (BOARD_ORIGIN_X + x * CARD_WIDTH, BOARD_ORIGIN_Y), 
                         (BOARD_ORIGIN_X + x * CARD_WIDTH, BOARD_ORIGIN_Y + GRID_SIZE * CARD_HEIGHT))
    for y in range(GRID_SIZE + 1):
        pygame.draw.line(DISPLAYSURF, BLACK, 
                         (BOARD_ORIGIN_X, BOARD_ORIGIN_Y + y * CARD_HEIGHT), 
                         (BOARD_ORIGIN_X + GRID_SIZE * CARD_WIDTH, BOARD_ORIGIN_Y + y * CARD_HEIGHT))

# Function to draw the board
def draw_board():
    DISPLAYSURF.blit(BG_board_IMAGE, (0,0))
    # music buttons V
    DISPLAYSURF.blit(pause_image, pause_button_rect.topleft)  # Pause button
    DISPLAYSURF.blit(play_image, play_button_rect.topleft)    # Play button
    DISPLAYSURF.blit(vol_up_img, volume_up_rect.topleft) # Volume up button
    DISPLAYSURF.blit(vol_dn_img, volume_down_rect.topleft) # Volume down button
    # music buttons ^
    draw_grid()
    red_count, blue_count = 0, 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col]:
                x = BOARD_ORIGIN_X + col * CARD_WIDTH
                y = BOARD_ORIGIN_Y + row * CARD_HEIGHT
                board[row][col].rect.topleft = (x, y)
                board[row][col].draw(DISPLAYSURF)
                if board[row][col].team == 'red':
                    red_count += 1
                else:
                    blue_count += 1
                    
    for card in red_cards:
        card.draw(DISPLAYSURF)
    for card in blue_cards:
        card.draw(DISPLAYSURF)

    # Draw the score indicators
    font = pygame.font.Font('fonts/adon/Adon Black.otf', 36)
    red_score_text = font.render(f'Red: {red_count}', True, RED)
    blue_score_text = font.render(f'Blue: {blue_count}', True, BLUE)
    DISPLAYSURF.blit(red_score_text, (BOARD_ORIGIN_X - CARD_WIDTH * 1.5, BOARD_ORIGIN_Y - 50))
    DISPLAYSURF.blit(blue_score_text, (BOARD_ORIGIN_X + GRID_SIZE * CARD_WIDTH + CARD_WIDTH // 2, BOARD_ORIGIN_Y - 50))

    # Draw the mode indicators
    font = pygame.font.Font(None, 25)
    same_mode_text = font.render(f'Same Mode: {"ON" if same_mode_enabled else "OFF"}', True, BLACK)
    plus_mode_text = font.render(f'Plus Mode: {"ON" if plus_mode_enabled else "OFF"}', True, BLACK)
    DISPLAYSURF.blit(same_mode_text, (10, 900)) # sets position of the same mode rect on dsiplay
    DISPLAYSURF.blit(plus_mode_text, (10, 930)) # sets position of the plus mode rect on dsiplay
    
def display_card_statement(statement):
    statement_rect = pygame.Rect(220, WINDOW_HEIGHT - 100, WINDOW_WIDTH - 430, 50)  # Rect at bottom of the screen
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), statement_rect)  # Black background
    pygame.draw.rect(DISPLAYSURF, (255, 255, 255), statement_rect, 2)  # White border

    font = pygame.font.Font(None, 24)  # Font for the statement text
    statement_text = font.render(statement, True, (255, 255, 255))  # White text
    text_rect = statement_text.get_rect(center=statement_rect.center)
    DISPLAYSURF.blit(statement_text, text_rect)

# Function to place a card on the board
def place_card(row, col, card):
    # Place the card on the board at the specified row and column
    board[row][col] = card
    
    # Directions list to check for adjacent cards
    # Format: (row offset, column offset, side index of placed card, side index of adjacent card)
    directions = [(-1, 0, 0, 1),  # Upwards (top side of the placed card)
                  (1, 0, 1, 0),   # Downwards (bottom side of the placed card)
                  (0, -1, 2, 3),  # Left (left side of the placed card)
                  (0, 1, 3, 2)]   # Right (right side of the placed card)
    
    # Loop through each direction to check adjacent cards
    for dr, dc, s1, s2 in directions:
        # Calculate the position of the adjacent card
        r, c = row + dr, col + dc
        
        # Check if the adjacent position is within bounds and has a card
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c]:
            # If the side of the placed card is stronger than the adjacent card's side
            if card.sides[s1] > board[r][c].sides[s2]:
                # Flip the adjacent card to the team of the placed card
                board[r][c].animate_color_change(card.team)
    
    # "Same" rule check
    if same_mode_enabled:
        # List to keep track of adjacent cards with the same value
        same_adjacent = []
        
        # Loop through each direction to check adjacent cards for the "Same" rule
        for dr, dc, s1, s2 in directions:
            # Calculate the position of the adjacent card
            r, c = row + dr, col + dc
            
            # Check if the adjacent position is within bounds and has a card
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c]:
                # If the side of the placed card is equal to the adjacent card's side
                if card.sides[s1] == board[r][c].sides[s2]:
                    # Add the adjacent card to the same_adjacent list
                    same_adjacent.append((r, c))
        
        # If there are two or more adjacent cards with the same value
        if len(same_adjacent) >= 2:
            # Flip all the adjacent cards with the same value to the team of the placed card
            for r, c in same_adjacent:
                board[r][c].animate_color_change(card.team)
    
    # "Plus" rule check
    if plus_mode_enabled:
        # List to keep track of adjacent cards satisfying the "Plus" rule
        plus_adjacent = []
        
        # Loop through each pair of directions to check for the "Plus" rule
        for i, (dr1, dc1, s1a, s2a) in enumerate(directions):
            # Calculate the position of the first adjacent card
            r1, c1 = row + dr1, col + dc1
            
            for j, (dr2, dc2, s1b, s2b) in enumerate(directions):
                # Ensure that the two directions are different
                if i != j:
                    # Calculate the position of the second adjacent card
                    r2, c2 = row + dr2, col + dc2
                    
                    # Check if both adjacent positions are within bounds and have cards
                    if (0 <= r1 < GRID_SIZE and 0 <= c1 < GRID_SIZE and 
                        0 <= r2 < GRID_SIZE and 0 <= c2 < GRID_SIZE and 
                        board[r1][c1] and board[r2][c2]):
                        
                        # If the sum of the sides of the placed card and the first adjacent card
                        # equals the sum of the sides of the placed card and the second adjacent card
                        if card.sides[s1a] + board[r1][c1].sides[s2a] == card.sides[s1b] + board[r2][c2].sides[s2b]:
                            # Add both adjacent cards to the plus_adjacent list
                            plus_adjacent.append((r1, c1))
                            plus_adjacent.append((r2, c2))
        
        # If the "Plus" rule condition is met
        if plus_adjacent:
            # Flip all the adjacent cards that satisfy the "Plus" rule to the team of the placed card
            for r, c in plus_adjacent:
                board[r][c].animate_color_change(card.team)


# card move animation V
def animate_card_movement(card, start_pos, end_pos, duration=550, arc_height=500):
    """Animates a card moving from start_pos to end_pos over a given duration with an arc."""
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()  # Record the start time
    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        # Calculate how far along the animation we are (a value between 0 and 1)
        t = min(elapsed_time / duration, 1)

        # Linear interpolation for horizontal (x-axis) movement
        new_x = (1 - t) * start_pos[0] + t * end_pos[0]

        # Parabolic interpolation for vertical (y-axis) movement
        # We use a parabola formula: arc_offset = arc_height * (1 - (2*t - 1)^2)
        # This gives the card a curved movement, peaking in the middle
        midpoint_x = (start_pos[0] + end_pos[0]) / 2
        arc_offset = arc_height * (1 - (2 * t - 1) ** 2)  # This creates the arc
        new_y = (1 - t) * start_pos[1] + t * end_pos[1] - arc_offset

        # Update card's position
        card.rect.topleft = (new_x, new_y)

        # Redraw the screen
        DISPLAYSURF.fill(BLACK)
        draw_board()
        for c in red_cards:
            c.draw(DISPLAYSURF)
        for c in blue_cards:
            c.draw(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, YELLOW, card.rect.inflate(10, 10), 3)  # Optional: Highlight the moving card
        pygame.display.update()

        # If the animation is complete, break out of the loop
        if t >= 1:
            break

        # Control the frame rate
        clock.tick(60)  # 60 frames per second
# card move animation ^


# AI player code here v
def score_card(card):
    """Simple scoring system: sum of the card's sides."""
    return sum(card.sides)

def score_position_control(row, col):
    """Score a position based on its control value (center, edges, corners)."""
    if row == GRID_SIZE // 2 and col == GRID_SIZE // 2:  # Center
        return 5  # High control score for the center
    elif row in [0, GRID_SIZE - 1] and col in [0, GRID_SIZE - 1]:  # Corners
        return 3  # Lower score for corners
    elif row in [0, GRID_SIZE - 1] or col in [0, GRID_SIZE - 1]:  # Edges
        return 2  # Medium score for edges
    return 1  # Default score for non-strategic positions

def score_blocking_player(row, col, card):
    """Score based on how well this move blocks the player's moves."""
    score = 0

    # Check neighboring positions to see if we can block a player move
    if row > 0 and board[row - 1][col]:  # Above
        neighbor = board[row - 1][col]
        if neighbor.team == player_team:
            score += card.sides[0] - neighbor.sides[1]  # Compare top of current card with bottom of player card

    if row < GRID_SIZE - 1 and board[row + 1][col]:  # Below
        neighbor = board[row + 1][col]
        if neighbor.team == player_team:
            score += card.sides[1] - neighbor.sides[0]  # Compare bottom of current card with top of player card

    if col > 0 and board[row][col - 1]:  # Left
        neighbor = board[row][col - 1]
        if neighbor.team == player_team:
            score += card.sides[2] - neighbor.sides[3]  # Compare left of current card with right of player card

    if col < GRID_SIZE - 1 and board[row][col + 1]:  # Right
        neighbor = board[row][col + 1]
        if neighbor.team == player_team:
            score += card.sides[3] - neighbor.sides[2]  # Compare right of current card with left of player card

    return score

def score_future_potential(row, col):
    """Score based on how many future moves are possible after placing a card."""
    potential_moves = 0

    # Count how many adjacent positions are open (can place future cards)
    if row > 0 and board[row - 1][col] is None:  # Above
        potential_moves += 1
    if row < GRID_SIZE - 1 and board[row + 1][col] is None:  # Below
        potential_moves += 1
    if col > 0 and board[row][col - 1] is None:  # Left
        potential_moves += 1
    if col < GRID_SIZE - 1 and board[row][col + 1] is None:  # Right
        potential_moves += 1

    return potential_moves

def ai_select_best_card():
    """AI selects the best card based on the scoring system."""
    available_cards = blue_cards if ai_team == 'blue' else red_cards

    if available_cards:
        # Select the card with the highest score
        best_card = max(available_cards, key=score_card)
        return best_card
    return None

def score_position(row, col, card):
    """Evaluate the score of placing a card at a given position on the grid."""
    control_weight = 1.5
    block_weight = 2.0
    future_weight = 1.0
    strength_weight = 1.0

    # Calculate score based on different factors
    control_score = score_position_control(row, col) * control_weight
    blocking_score = score_blocking_player(row, col, card) * block_weight
    future_score = score_future_potential(row, col) * future_weight
    strength_score = score_card(card) * strength_weight

    # Combine the scores
    total_score = control_score + blocking_score + future_score + strength_score
    return total_score

def ai_find_best_position(card):
    """Find the best position for a given card based on the scoring system."""
    best_position = None
    best_score = float('-inf')

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:  # Check if the position is empty
                position_score = score_position(row, col, card)
                if position_score > best_score:
                    best_score = position_score
                    best_position = (row, col)

    return best_position

def ai_make_move():
    global current_team

    # AI selects the best card based on the scoring system
    selected_card = ai_select_best_card()

    if selected_card:
        # AI selects the best position to place the card
        best_position = ai_find_best_position(selected_card)

        if best_position:
            row, col = best_position

            # Animate the card moving from the deck to the grid
            start_pos = selected_card.rect.topleft
            end_pos = (BOARD_ORIGIN_X + col * CARD_WIDTH, BOARD_ORIGIN_Y + row * CARD_HEIGHT)
            animate_card_movement(selected_card, start_pos, end_pos)

            # Place the card on the grid after the animation
            place_card(row, col, selected_card)
            (blue_cards if ai_team == 'blue' else red_cards).remove(selected_card)

            # Switch back to the player's turn
            current_team = player_team

                
# AI player code here ^
def show_image_carousel_screen():
    """Display an image carousel screen."""
    images = [
        pygame.image.load('images/tutorial_pics/game_asset_tutorialPanel_one.png'),
        pygame.image.load('images/tutorial_pics/game_asset_tutorialPanel_two.png'),
        pygame.image.load('images/tutorial_pics/game_asset_tutorialPanel_plusRule_one.png'),
        pygame.image.load('images/tutorial_pics/game_asset_tutorialPanel_plusRule_two.png'),
        pygame.image.load('images/tutorial_pics/game_asset_tutorialPanel_sameRule_one.png'),
        pygame.image.load('images/tutorial_pics/game_asset_tutorialPanel_sameRule_two.png')
    ]

    # Corresponding descriptions for the images
    descriptions = [
        """RULES:
        If a card is place on the board. 
        And that card's side is a higher value
         than the opponent's card's side.
        then the opponent's card is deafeated.""",
        """the winner is determined by which
        team has more cards are on the board.
        So try to get as many cards to your
        team's color as possible.""",
        """With the 'PLUS' rule active: If a card
        played on the board has two side values
        that equal the same number when added to 
        an opponent card's side value.
        you deafeat the opponent cards.""",
        """this works even if
        the card you played has
         lower side-wall values
        than the opponent's card.""",
        """With the 'SAME' rule active:
        if a card played on the board
        has two side-wall values
        that are the same as
        an opponent card's side-wall value.""",
        """you defeat the oppenent cards.
        even if the card you played 
        has lower side-wall values
        than the opponent's card."""
    ]

    # Scale images to fit the rectangle area
    rect_width, rect_height = 500, 700  # Dimensions of the display rectangle
    images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in images]

    current_image_index = 0

    # Define display rectangle position
    rect_x = (WINDOW_WIDTH - rect_width) // 2
    rect_y = (WINDOW_HEIGHT - rect_height) // 2 - 50


    # Define button dimensions
    left_arrow = pygame.Rect(50, WINDOW_HEIGHT // 2 - 25, 50, 50)
    right_arrow = pygame.Rect(WINDOW_WIDTH - 100, WINDOW_HEIGHT // 2 - 25, 50, 50)
    # Load the "Back to Title" button image
    next_button_image = pygame.image.load('images/backgrounds/game_asset_buttonholder.png')
    next_button_image = pygame.transform.scale(next_button_image, (225, 125))  # Scale the image to the button size
    next_button_rect = next_button_image.get_rect(topleft=(WINDOW_WIDTH // 2 + 350, WINDOW_HEIGHT - 150)) # position of button

    font = pygame.font.Font('fonts/adon/Adon Black.otf', 13)
    back_btn_font = pygame.font.Font('fonts/adon/Adon Black.otf', 25)
    next_text = back_btn_font.render("BACK", True, WHITE)

    description_image = pygame.image.load('images/backgrounds/game_asset_textholder.png')  # Load the background image for the description
    description_image = pygame.transform.scale(description_image, (rect_width, 250))  # Scale to fit the description area

    # description_rect = pygame.Rect(rect_x, rect_y + rect_height + 20, rect_width, 100)  # Below image

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if left_arrow.collidepoint(event.pos):
                    current_image_index = (current_image_index - 1) % len(images)
                elif right_arrow.collidepoint(event.pos):
                    current_image_index = (current_image_index + 1) % len(images)
                elif next_button_rect.collidepoint(event.pos):
                    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
                    show_title_screen()
                    return

        # Draw the background and current image
        DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0,0)) 
        pygame.draw.rect(DISPLAYSURF, WHITE, (rect_x, rect_y, rect_width, rect_height), 2)  # Draw border for the image area
        DISPLAYSURF.blit(images[current_image_index], (rect_x, rect_y))

        # Draw description rectangle and text
        
        DISPLAYSURF.blit(description_image, (rect_x, rect_y + rect_height - 25))
         # Render description text as multiple lines
        lines = descriptions[current_image_index].split("\n")
        line_height = 20  # Space between lines
        for i, line in enumerate(lines):
            description_text = font.render(line.strip(), True, WHITE)
            description_text_rect = description_text.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height + 68 + i * line_height)) # change '60' to move text in desciption image up or down
            DISPLAYSURF.blit(description_text, description_text_rect)

        # Draw arrows
        pygame.draw.rect(DISPLAYSURF, WHITE, left_arrow)
        pygame.draw.polygon(DISPLAYSURF, BLACK, [(60, WINDOW_HEIGHT // 2), (90, WINDOW_HEIGHT // 2 - 20), (90, WINDOW_HEIGHT // 2 + 20)])

        pygame.draw.rect(DISPLAYSURF, WHITE, right_arrow)
        pygame.draw.polygon(DISPLAYSURF, BLACK, [(WINDOW_WIDTH - 60, WINDOW_HEIGHT // 2), (WINDOW_WIDTH - 90, WINDOW_HEIGHT // 2 - 20), (WINDOW_WIDTH - 90, WINDOW_HEIGHT // 2 + 20)])

        # Draw "Back to Title" button image
        DISPLAYSURF.blit(next_button_image, next_button_rect.topleft)

        # Draw "Back to Title" text on top of the button
        next_text_rect = next_text.get_rect(center=next_button_rect.center)
        DISPLAYSURF.blit(next_text, next_text_rect)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def gallery_mode():
    "List to stor images for gallery"
    pictures = [
        pygame.image.load('images/card/green_bat.png'),
        pygame.image.load('images/card/Lion_hunter.png'),
        pygame.image.load('images/card/red_cultist.png'),
        pygame.image.load('images/card/IMG_0946.png'),
        pygame.image.load('images/card/Hecterra.png')
        
    ]

    # Scale images to fit the rectangle area
    rect_width, rect_height = 650, 950  # Dimensions of the display rectangle
    pictures = [pygame.transform.scale(pic, (rect_width, rect_height)) for pic in pictures]

    current_picture_index = 0

    # Define display rectangle position
    rect_x = (WINDOW_WIDTH - rect_width) // 2
    rect_y = (WINDOW_HEIGHT - rect_height) // 2 - 50

    # Define button dimensions
    left_arrow = pygame.Rect(50, WINDOW_HEIGHT // 2 - 25, 50, 50)
    right_arrow = pygame.Rect(WINDOW_WIDTH - 100, WINDOW_HEIGHT // 2 - 25, 50, 50)
    # Load the "Back to Title" button image
    back_button_image = pygame.image.load('images/backgrounds/game_asset_buttonholder.png')
    back_button_image = pygame.transform.scale(back_button_image, (225, 125))  # Scale the image to the button size
    back_button_rect = back_button_image.get_rect(topleft=(WINDOW_WIDTH // 2 + 350, WINDOW_HEIGHT - 150)) # position of button

    font = pygame.font.Font('fonts/adon/Adon Black.otf', 13)
    back_btn_font = pygame.font.Font('fonts/adon/Adon Black.otf', 25)
    back_text = back_btn_font.render("BACK", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if left_arrow.collidepoint(event.pos):
                    current_picture_index = (current_picture_index - 1) % len(pictures)
                elif right_arrow.collidepoint(event.pos):
                    current_picture_index = (current_picture_index + 1) % len(pictures)
                elif back_button_rect.collidepoint(event.pos):
                    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
                    show_title_screen()
                    return
                
    # Draw the background and current image
        DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0,0)) 
        pygame.draw.rect(DISPLAYSURF, WHITE, (rect_x, rect_y, rect_width, rect_height), 2)  # Draw border for the image area
        DISPLAYSURF.blit(pictures[current_picture_index], (rect_x, rect_y))

        # Draw arrows
        pygame.draw.rect(DISPLAYSURF, WHITE, left_arrow)
        pygame.draw.polygon(DISPLAYSURF, BLACK, [(60, WINDOW_HEIGHT // 2), (90, WINDOW_HEIGHT // 2 - 20), (90, WINDOW_HEIGHT // 2 + 20)])

        pygame.draw.rect(DISPLAYSURF, WHITE, right_arrow)
        pygame.draw.polygon(DISPLAYSURF, BLACK, [(WINDOW_WIDTH - 60, WINDOW_HEIGHT // 2), (WINDOW_WIDTH - 90, WINDOW_HEIGHT // 2 - 20), (WINDOW_WIDTH - 90, WINDOW_HEIGHT // 2 + 20)])

        # Draw "Back to Title" button image
        DISPLAYSURF.blit(back_button_image, back_button_rect.topleft)

        # Draw "Back to Title" text on top of the button
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        DISPLAYSURF.blit(back_text, back_text_rect)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)
# Function to display the title screen
def show_title_screen():
    DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0,0))
    font = pygame.font.Font('fonts/stencil_gothic/Gothic Stencil - Dker.ttf', 74)
    text = font.render('Vionarch', True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    DISPLAYSURF.blit(text, text_rect)

    font = pygame.font.Font('fonts/adon/Adon Black.otf', 50)
    text = font.render('Press any key to start', True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    DISPLAYSURF.blit(text, text_rect)

    button_image = pygame.image.load('images/backgrounds/game_asset_buttonholder_forMain.png')
    button_image = pygame.transform.scale(button_image, (230, 80))  # Scale the button image

    # Button for image carousel v
    carousel_button_rect = button_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150))
    DISPLAYSURF.blit(button_image, carousel_button_rect.topleft)
    carousel_font = pygame.font.Font('fonts/aesthico/Aesthico(Demo)-Regular.ttf', 22)
    carousel_text = carousel_font.render('Tutorial', True, WHITE)
    carousel_text_rect = carousel_text.get_rect(center=carousel_button_rect.center)
    DISPLAYSURF.blit(carousel_text, carousel_text_rect)
    # Button for image carousel ^

    # Button for Gallery mode v
    gallery_button_rect = button_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 240))
    DISPLAYSURF.blit(button_image, gallery_button_rect.topleft)
    gallery_font = pygame.font.Font('fonts/aesthico/Aesthico(Demo)-Regular.ttf', 22)
    gallery_text = gallery_font.render('Gallery', True, WHITE)
    gallery_text_rect = gallery_text.get_rect(center=gallery_button_rect.center)
    DISPLAYSURF.blit(gallery_text, gallery_text_rect)
    # Button for Gallery mode ^
    

    pygame.display.update()
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if carousel_button_rect.collidepoint(event.pos):
                    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
                    show_image_carousel_screen()
                    waiting = False
                    return
                # this elif loop needed to be insdie the one above
                elif event.type == MOUSEBUTTONDOWN:
                    if gallery_button_rect.collidepoint(event.pos):
                        fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
                        gallery_mode()
                        waiting = False
                        return
            elif event.type == KEYDOWN:
                fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
                # show_team_selection_screen() <--- this was making the team selection game show twice
                waiting = False
                return # may need to remove

    selection_is_made_sound.play()
    
    

    

# Function to display the team selection screen with "Same" and "Plus" mode options
def show_team_selection_screen():
    
    DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0, 0))
    font = pygame.font.Font('fonts/adon/Adon Black.otf', 40)
    mode_info_font = pygame.font.Font('fonts/adon/Adon Black.otf', 20)
    
    
    # Render the team selection texts
    red_text = font.render('Red Team', True, RED)
    blue_text = font.render('Blue Team', True, BLUE)
    red_rect = red_text.get_rect(center=(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
    blue_rect = blue_text.get_rect(center=(3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
    
    # Render the mode texts (same mode and plus mode)
    same_mode_text = font.render('Same Mode: OFF', True, BLACK)
    same_mode_rect = same_mode_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
    plus_mode_text = font.render('Plus Mode: OFF', True, BLACK)
    plus_mode_rect = plus_mode_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))

    # back to title from team selection v
    button_image = pygame.image.load('images/backgrounds/game_asset_buttonholder_forMain.png')
    button_image = pygame.transform.scale(button_image, (230, 80))  # Scale the button image
    back_to_title_button_rect = button_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150))
    DISPLAYSURF.blit(button_image, back_to_title_button_rect.topleft)
    back_to_title_font = pygame.font.Font('fonts/aesthico/Aesthico(Demo)-Regular.ttf', 22)
    back_to_title_text = back_to_title_font.render('Back to Title', True, WHITE)
    back_to_title_text_rect = back_to_title_text.get_rect(center=back_to_title_button_rect.center)
    DISPLAYSURF.blit(back_to_title_text, back_to_title_text_rect)
    # back to title from team selection ^
    
    # Blit the initial texts to the display surface
    DISPLAYSURF.blit(red_text, red_rect)
    DISPLAYSURF.blit(blue_text, blue_rect)
    DISPLAYSURF.blit(same_mode_text, same_mode_rect)
    DISPLAYSURF.blit(plus_mode_text, plus_mode_rect)
    pygame.display.update()
    
    # Initialize global variables
    global player_team, ai_team, same_mode_enabled, plus_mode_enabled
    choosing = True
    same_mode_enabled = False
    plus_mode_enabled = False

    same_mode_description = ''
    plus_mode_description = ''
    
    while choosing:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # Check if player selected Red or Blue team
                if red_rect.collidepoint(event.pos):
                    player_team = 'red'
                    ai_team = 'blue'  # AI gets the opposite team
                    choosing = False
                elif blue_rect.collidepoint(event.pos):
                    player_team = 'blue'
                    ai_team = 'red'  # AI gets the opposite team
                    choosing = False
                
                # Toggle Same Mode
                elif same_mode_rect.collidepoint(event.pos):
                    same_mode_enabled = not same_mode_enabled
                    same_mode_text = font.render(f'Same Mode: {"ON" if same_mode_enabled else "OFF"}', True, BLACK)
                    # Display or hide description
                    if same_mode_enabled:
                        same_mode_description = "In Same Mode, cards with matching numbers defeat adjacent cards."
                    else:
                        same_mode_description = ""
                
                # Toggle Plus Mode
                elif plus_mode_rect.collidepoint(event.pos):
                    plus_mode_enabled = not plus_mode_enabled
                    plus_mode_text = font.render(f'Plus Mode: {"ON" if plus_mode_enabled else "OFF"}', True, BLACK)
                    # Display or hide description
                    if plus_mode_enabled:
                        plus_mode_description = "In Plus Mode, cards with matching sums defeat adjacent cards."
                    else:
                        plus_mode_description = ""

                # Back to Title button
                elif back_to_title_button_rect.collidepoint(event.pos):
                    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
                    show_title_screen()
                    # return <-- this was causeing the team select screen to be skipped after key press to go to team select

                    
                    
                # Redraw everything after an update
                DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0, 0))
                DISPLAYSURF.blit(red_text, red_rect)
                DISPLAYSURF.blit(blue_text, blue_rect)
                DISPLAYSURF.blit(same_mode_text, same_mode_rect)
                DISPLAYSURF.blit(plus_mode_text, plus_mode_rect)
                # makes sure that back to title image and btn are on screen after clicked v
                DISPLAYSURF.blit(button_image, back_to_title_button_rect.topleft)
                DISPLAYSURF.blit(back_to_title_text, back_to_title_text_rect)

                # Blit mode descriptions only if they are non-empty
                if same_mode_description:
                    same_mode_description_text = mode_info_font.render(same_mode_description, True, BLACK)
                    same_mode_description_rect = same_mode_description_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 130))
                    DISPLAYSURF.blit(same_mode_description_text, same_mode_description_rect)

                if plus_mode_description:
                    plus_mode_description_text = mode_info_font.render(plus_mode_description, True, BLACK)
                    plus_mode_description_rect = plus_mode_description_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 180))
                    DISPLAYSURF.blit(plus_mode_description_text, plus_mode_description_rect)

            

                pygame.display.update()

    # Optional fade-out effect after selection
    selection_is_made_sound.play()
    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)

# Turn indicator
def display_current_player():
    font = pygame.font.Font('fonts/aesthico/Aesthico(Demo)-Regular.ttf', 20)
    current_player_text = font.render(f"Current Turn: {'Red' if current_team == 'red' else 'Blue'}", True, BLACK)
    DISPLAYSURF.blit(current_player_text, (BOARD_ORIGIN_X, WINDOW_HEIGHT - 50))

# Function to display the game over screen
def show_game_over_screen(winner):
    # Load the video
    if "Win" in winner:
        video_clip = VideoFileClip('videos/alpha_awesome_small.avi') # shrank file for github but still didnt work...
            
            # Set up the timing for the video playback
        video_duration = video_clip.duration  # Get the length of the video
        start_time = pygame.time.get_ticks()  # Record the start time

            # Define the rect for the video area at the top (e.g., 1/3 of the screen)
        video_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 3)

        while (pygame.time.get_ticks() - start_time) < (video_duration * 1000):  # Play video during its duration
                # Clear screen first
            DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0, 0))
                
                # Get the current frame from the video (based on time)
            frame = video_clip.get_frame((pygame.time.get_ticks() - start_time) / 1000)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                
                # Scale the frame to fit inside the defined video area
            frame_surface = pygame.transform.scale(frame_surface, (video_rect.width, video_rect.height))
                
            frame_surface.set_colorkey(BLACK)  # can Treat pure black or white as transparent
                # Display the video frame
            DISPLAYSURF.blit(frame_surface, video_rect.topleft)

                # Draw the game over text and buttons underneath the video
            font = pygame.font.Font('fonts/aesthico/Aesthico(Demo)-Regular.ttf', 60)
            text = font.render(f'{winner}!', True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            DISPLAYSURF.blit(text, text_rect)

            font = pygame.font.Font('fonts/adon/Adon Black.otf', 50)
            new_game_text = font.render('New Game?', True, GREEN)
            new_game_rect = new_game_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            DISPLAYSURF.blit(new_game_text, new_game_rect)

            pygame.display.update()

                # Handle quitting or interacting with buttons during video playback
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if new_game_rect.collidepoint(event.pos):
                        new_game_sound.set_volume(0.3)
                        new_game_sound.play()  # Sound effect for new game selected
                        fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
                        initialize_board()
                        show_team_selection_screen()
                        return  # Exit function to start a new game

            FPS_CLOCK.tick(60)  # Control the frame rate

    # After the video finishes, display the same game over screen (without video)
    DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0, 0))
    font = pygame.font.Font('fonts/aesthico/Aesthico(Demo)-Regular.ttf', 60)
    text = font.render(f'{winner}!', True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    DISPLAYSURF.blit(text, text_rect)

    font = pygame.font.Font('fonts/adon/Adon Black.otf', 50)
    new_game_text = font.render('New Game?', True, GREEN)
    new_game_rect = new_game_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    DISPLAYSURF.blit(new_game_text, new_game_rect)
    pygame.display.update()

    # Wait for player interaction (after video has finished)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if new_game_rect.collidepoint(event.pos):
                    new_game_sound.set_volume(0.3)
                    new_game_sound.play()  # Sound effect for new game selected
                    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
                    initialize_board()
                    show_team_selection_screen()
                    waiting = False


# Check if the board is full
def is_board_full():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                return False
    return True

# Main game loop
show_title_screen()
show_team_selection_screen()

# where i think the async function should go?
# async def main():
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Handle pause/play/volume controls for music...
            if pause_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.mixer.music.pause()
            elif play_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.mixer.music.unpause()
            elif volume_up_rect.collidepoint(mouse_x, mouse_y):
                current_volume = min(1.0, current_volume + 0.1)
                pygame.mixer.music.set_volume(current_volume)
            elif volume_down_rect.collidepoint(mouse_x, mouse_y):
                current_volume = max(0.0, current_volume - 0.1)
                pygame.mixer.music.set_volume(current_volume)

            # Handle card dragging if no music button is clicked
            else:
                if current_team == player_team:  # Ensure it's the player's turn
                    for card in red_cards if player_team == 'red' else blue_cards:
                        if card.rect.collidepoint(event.pos):
                            dragging_card = card
                            # Define drag offsets when the card is clicked
                            drag_offset_x = card.rect.x - mouse_x
                            drag_offset_y = card.rect.y - mouse_y
                            break

        elif event.type == MOUSEBUTTONUP:
            if dragging_card and current_team == player_team:  # Ensure it's the player's turn
                mouse_x, mouse_y = event.pos
                row = (mouse_y - BOARD_ORIGIN_Y) // CARD_HEIGHT
                col = (mouse_x - BOARD_ORIGIN_X) // CARD_WIDTH
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and board[row][col] is None:
                    place_card(row, col, dragging_card)
                    if dragging_card in red_cards:
                        red_cards.remove(dragging_card)
                    if dragging_card in blue_cards:
                        blue_cards.remove(dragging_card)
                    current_team = ai_team  # Switch to the AI after the player moves
                dragging_card = None

        elif event.type == MOUSEMOTION and current_team == player_team:
            if dragging_card:
                mouse_x, mouse_y = event.pos
                # Update the position of the card based on the drag offsets
                dragging_card.rect.topleft = (mouse_x + drag_offset_x, mouse_y + drag_offset_y)

        # Handle arrow key navigation
        elif event.type == KEYDOWN and current_team == player_team:
            # Determine the deck based on the current team (only player uses arrow keys)
            deck = red_cards if player_team == 'red' else blue_cards

            if selection_mode == DECK_SELECTION:
                if deck:  # Only navigate if the deck has cards
                    # Navigate through the deck with arrow keys
                    if event.key == pygame.K_UP or event.key == pygame.K_LEFT:  # Move up/left in the deck
                        selected_card_index = (selected_card_index - 1) % len(deck)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:  # Move down/right in the deck
                        selected_card_index = (selected_card_index + 1) % len(deck)

                    # Ensure selected_card_index is within bounds of the current deck
                    selected_card_index = min(selected_card_index, len(deck) - 1)  # Ensure index is within bounds
                    selected_card = deck[selected_card_index]

                    # When Enter or Space is pressed, select the card and switch to grid selection mode
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        selection_mode = GRID_SELECTION  # Switch to grid selection

            elif selection_mode == GRID_SELECTION:
                # Navigate through the grid with arrow keys
                if event.key == pygame.K_UP:  # Move up on the grid
                    grid_row = max(0, grid_row - 1)
                elif event.key == pygame.K_DOWN:  # Move down on the grid
                    grid_row = min(GRID_SIZE - 1, grid_row + 1)
                elif event.key == pygame.K_LEFT:  # Move left on the grid
                    grid_col = max(0, grid_col - 1)
                elif event.key == pygame.K_RIGHT:  # Move right on the grid
                    grid_col = min(GRID_SIZE - 1, grid_col + 1)

                # Place the selected card using Enter or Space, then switch back to deck selection mode
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if board[grid_row][grid_col] is None:
                        # Get the card's current position (from the deck)
                        start_pos = selected_card.rect.topleft

                        # Calculate the target position on the grid
                        end_pos = (BOARD_ORIGIN_X + grid_col * CARD_WIDTH, BOARD_ORIGIN_Y + grid_row * CARD_HEIGHT)

                        # Animate the card moving from the deck to the grid
                        animate_card_movement(selected_card, start_pos, end_pos)
                        place_card(grid_row, grid_col, selected_card)
                        deck.remove(selected_card)

                        # Reset index only if deck still has cards
                        if deck:
                            selected_card_index = 0  # Reset selected index if there are cards left

                        current_team = ai_team  # Switch to AI's turn after player's move
                        selection_mode = DECK_SELECTION  # Switch back to deck selection mode

    # ---- AI Move Section ----
    if current_team == ai_team:
        ai_make_move()  # Let the AI make its move
        current_team = player_team  # After AI's move, switch back to player

    # ---- Drawing Section ----
    DISPLAYSURF.fill(BLACK)  # Clear the screen with a background color (BLACK)

    # Draw the game board first
    draw_board()

    if selection_mode == GRID_SELECTION:
        # Highlight the current grid cell for card placement
        pygame.draw.rect(DISPLAYSURF, YELLOW, 
                         (BOARD_ORIGIN_X + grid_col * CARD_WIDTH, BOARD_ORIGIN_Y + grid_row * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT), 3)

    # Draw the deck of cards for the current player (either red or blue team)
    for card in red_cards:
        card.draw(DISPLAYSURF)  # Draw all red team cards
    for card in blue_cards:
        card.draw(DISPLAYSURF)  # Draw all blue team cards

    # Determine the deck based on the current player's team for highlighting
    deck = red_cards if player_team == 'red' else blue_cards

    if selection_mode == DECK_SELECTION:
        # Highlight the currently selected card in the deck
        if deck:  # Ensure the deck has cards before trying to highlight
            selected_card = red_cards[selected_card_index] if player_team == 'red' else blue_cards[selected_card_index]
            pygame.draw.rect(DISPLAYSURF, YELLOW, selected_card.rect.inflate(10, 10), 3)  # Draw yellow border around selected card
             # Display the card's statement at the bottom of the screen
            display_card_statement(selected_card.statement)
    # Draw the current player
    display_current_player()

    # Check for game over
    if is_board_full():
        pygame.display.update()
        pygame.time.delay(1000)  # 2-second delay
        fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)

        red_count = sum(card.team == 'red' for row in board for card in row if card)
        blue_count = sum(card.team == 'blue' for row in board for card in row if card)

        if red_count > blue_count:
            if player_team == 'red':
                winner = 'You Win'
            else:
                winner = 'You Lose'
        elif blue_count > red_count:
            if player_team == 'blue':
                winner = 'You Win'
            else:
                winner = 'You Lose'
        else:
            winner = 'Draw'
        # if red_count > blue_count:
        #     winner = 'Red Team'
        # elif blue_count > red_count:
        #     winner = 'Blue Team'
        # else:
        #     winner = 'Draw'

        
        show_game_over_screen(winner)

    # Refresh the display
    pygame.display.update()
    # "await asyncio.sleep(0)  # Very important, and keep it 0" maybe where this should go?
    FPS_CLOCK.tick(FPS)
    # asyncio.run(main()) .. and mybe finally here?

