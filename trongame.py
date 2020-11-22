# description: A two-player tron game. Player 1 (blue) moves
# using W (up), A (left), S, (down), and D (right). Player 2
# moves using arrow keys. Otherwise, both players move using
# joysticks. Both players must try to avoid hitting each other,
# the wall, and themselves.

# Import libraries
import pygame
import time
from sys import exit

# Initialize the game engine
pygame.init()
pygame.joystick.init()

# Define colours
black = (0, 0, 0)
grey = (89, 87, 87)
green = (0, 255, 0)
blue = (22, 191, 247)
pink = (242, 87, 240)
yellow = (255, 255, 0)

# Define boundaries of the window
x = 800
y = 600
size = [x, y]
screen = pygame.display.set_mode(size)

# Name the window
pygame.display.set_caption("Play Tron")


# Render the text
def text_format(message, textFont, textSize, textColour):
    '''
    Args:
        message: Text to display to surface (str).
        textFont: Font used (str).
        textSize: Size of text (int).
        textColour: Colour of text (tuple of three integers).

    Returns:
        Text for menu.
    '''
    # Font
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColour)
    return newText


# Framerate
clock = pygame.time.Clock()
FPS = 20


def run(p1_score, p2_score):
    '''Starts the game.

    Args:
        p1_score (int): The score of the first player before
        starting the game.
        p2_score (int): The score of the second player before
        starting the game.

    Returns:
        Updated scores for each player (int).
    '''

    # Sets the initial map
    screen.fill(black)
    for i in range(0, x, 20):
        pygame.draw.line(screen, grey, [i, 0], [i, y], 1)
    for i in range(0, y, 20):
        pygame.draw.line(screen, grey, [0, i], [x, i], 1)

    pygame.display.flip()

    # Variables for the first player
    p1_x = x / 4
    p1_y = y / 3
    p1_alive = True
    p1_colour = blue

    # Variables for the second player
    p2_x = (x * 3) / 4
    p2_y = (y * 2) / 3
    p2_alive = True
    p2_colour = pink

    # Assigns a boolean value to check whether or not the square
    # has been travelled already
    grid = [[False for temp in range(int(y / 20))] for temp in range(int(x / 20))]
    done = False

    # Sets the initial directions for the players
    directions = ["right", "left"]

    # Initializes clock
    clock = pygame.time.Clock()

    # Counts the number of joysticks
    joystick_count = pygame.joystick.get_count()

    while not done:
        for event in pygame.event.get():
            # Handles keyboard input
            if event.type == pygame.KEYDOWN:

                # To change the direction of player 1
                # depending on the key pressed
                if event.key == pygame.K_a:
                    if directions[0] != "right":
                        directions[0] = "left"
                elif event.key == pygame.K_d:
                    if directions[0] != "left":
                        directions[0] = "right"
                elif event.key == pygame.K_w:
                    if directions[0] != "down":
                        directions[0] = "up"
                elif event.key == pygame.K_s:
                    if directions[0] != "up":
                        directions[0] = "down"

                # To change the direction of player 2
                # depending on the key pressed
                elif event.key == pygame.K_RIGHT:
                    if directions[1] != "left":
                        directions[1] = "right"
                elif event.key == pygame.K_UP:
                    if directions[1] != "down":
                        directions[1] = "up"
                elif event.key == pygame.K_DOWN:
                    if directions[1] != "up":
                        directions[1] = "down"
                elif event.key == pygame.K_LEFT:
                    if directions[1] != "right":
                        directions[1] = "left"

        # To allow two joysticks to play the game
        for i in range(joystick_count):
            if i > 1:
                break
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            x_axis = joystick.get_axis(1)  # x axis
            y_axis = joystick.get_axis(0)  # y axis

            # To change the direction of the player
            # depending on the motion of the joystick
            if -0.5 <= x_axis <= 0.5:
                if y_axis >= 0.5 and directions[i] != "down":
                    directions[i] = "up"
                elif y_axis <= -0.5 and directions[i] != "up":
                    directions[i] = "down"
            elif -0.5 <= y_axis <= 0.5:
                if x_axis >= 0.5 and directions[i] != "left":
                    directions[i] = "right"
                elif x_axis <= -0.5 and directions[i] != "right":
                    directions[i] = "left"

        # Redraws the players based on their direction
        if p1_alive or p2_alive:
            pygame.draw.rect(screen, p1_colour, [
                p1_x + 1, p1_y + 1, (x / 40) - 1, (x / 40) - 1])
            pygame.draw.rect(screen, p2_colour, [
                p2_x + 1, p2_y + 1, (x / 40) - 1, (x / 40) - 1])
            pygame.display.flip()

        # Checks if player 1 will travel off the map
        if p1_x >= x or p1_x < 0 or p1_y >= y or p1_y < 0:
            p1_alive = False

        # Checks if player 1 will collide with another square
        else:
            if grid[int(p1_x / 20 - 1)][int(p1_y / 20 - 1)]:
                p1_alive = False
            # Sets player 1's square to True
            grid[int(p1_x / 20 - 1)][int(p1_y / 20 - 1)] = True

        # Checks if player 2 will travel off the map
        if p2_x >= x or p2_x < 0 or p2_y >= y or p2_y < 0:
            p2_alive = False

        # Checks if player 2 will collide with another square
        else:
            if grid[int(p2_x / 20 - 1)][int(p2_y / 20 - 1)]:
                p2_alive = False
            # Sets player 2's square to True
            grid[int(p2_x / 20 - 1)][int(p2_y / 20 - 1)] = True

        # Updates player 1's position if they have not collided
        p1_dir = directions[0]
        if p1_alive and p2_alive:
            if p1_dir == "left":
                p1_x -= 20
            elif p1_dir == "right":
                p1_x += 20
            elif p1_dir == "up":
                p1_y -= 20
            elif p1_dir == "down":
                p1_y += 20

        # Updates player 2's position if they have not collided
        p2_dir = directions[1]
        if p2_alive and p1_alive:
            if p2_dir == "left":
                p2_x -= 20
            elif p2_dir == "right":
                p2_x += 20
            elif p2_dir == "up":
                p2_y -= 20
            elif p2_dir == "down":
                p2_y += 20

        # Scoring Mechanism
        if not p1_alive or not p2_alive:
            if not p1_alive:
                p2_score += 1
            if not p2_alive:
                p1_score += 1
            done = True
            time.sleep(0.3)

        clock.tick(20)
    return p1_score, p2_score


# Menu
def main_menu():
    '''Menu screen for game.

    Returns:
        Updated main menu surface.
    '''

    # Initialize variables for main menu
    menu = True
    restart = False
    surface = pygame.display.set_mode(size)
    surface.fill(blue)
    p1_score = 0
    p2_score = 0

    while menu:
        s = "ANY KEY TO RESTART" if restart else "ANY KEY TO START"

        # Play again mechanism
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = False
                else:
                    restart = True
                    (p1_score, p2_score) = run(p1_score, p2_score)
            if event.type == pygame.JOYBUTTONDOWN:
                restart = True
                (p1_score, p2_score) = run(p1_score, p2_score)

        # Menu User Interface
        surface.fill(blue)
        font = "Retro.ttf"
        title = text_format("Play Tron", font, 90, yellow)
        text_start = text_format(s, font, 50, black)
        text_quit = text_format("ESC TO QUIT", font, 40, black)
        text_score = text_format("P1 SCORE: " + str(p1_score) +
                                 "         P2 SCORE: " + str(p2_score),
                                 font, 30, yellow)
        text_instructions1 = text_format("Welcome to two-player tron." +
                                         " If your snake crashes into",
                                         font, 16, black)
        text_instructions2 = text_format("your opponent's snake, the wall," +
                                         " or itself, it will die.",
                                         font, 16, black)
        text_instructions3 = text_format("If you are using a keyboard," +
                                         " player 1 moves using W (up), ",
                                         font, 16, black)
        text_instructions4 = text_format("A (left), S (down), and D (right)." +
                                         " Player 2 moves using",
                                         font, 16, black)
        text_instructions5 = text_format("arrow keys. Otherwise," +
                                         " use joysticks.",
                                         font, 16, black)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()
        score_rect = text_score.get_rect()
        instructions1_rect = text_instructions1.get_rect()
        instructions2_rect = text_instructions2.get_rect()
        instructions3_rect = text_instructions3.get_rect()
        instructions4_rect = text_instructions4.get_rect()
        instructions5_rect = text_instructions5.get_rect()

        # Menu Text
        surface.blit(title, (x / 2 - (title_rect[2] / 2), 50))
        surface.blit(text_start, (x / 2 - (start_rect[2] / 2), 180))
        surface.blit(text_quit, (x / 2 - (quit_rect[2] / 2), 250))
        surface.blit(text_score, (x / 2 - (score_rect[2] / 2), 340))
        surface.blit(text_instructions1,
                     (x / 2 - (instructions1_rect[2] / 2), 430))
        surface.blit(text_instructions2,
                     (x / 2 - (instructions2_rect[2] / 2), 450))
        surface.blit(text_instructions3,
                     (x / 2 - (instructions3_rect[2] / 2), 480))
        surface.blit(text_instructions4,
                     (x / 2 - (instructions4_rect[2] / 2), 500))
        surface.blit(text_instructions5,
                     (x / 2 - (instructions5_rect[2] / 2), 520))

        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Play Tron")


main_menu()
