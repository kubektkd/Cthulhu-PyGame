import pygame
from utils.constants import *
import utils.config as config
from utils.helpers import _, read_locale_file

pygame.init()

clock = pygame.time.Clock()
fps = config.fps

read_locale_file(config.default_lang)

screen = pygame.display.set_mode((config.screen_width, config.screen_height))
pygame.display.set_caption(_('title'))

# DEFINE FONTS
font = pygame.font.SysFont('Lucida Console', config.default_font_size)

# LOAD IMAGES
# background image
start_background = pygame.image.load('assets/img/Background/menu1.jpg').convert_alpha()
background_img = pygame.image.load('assets/img/Background/scene1.jpg').convert_alpha()
background_img2 = pygame.image.load('assets/img/Background/scene2.jpg').convert_alpha()
background_list = [background_img, background_img2, start_background]

# panel image
panel_img = pygame.image.load('assets/img/Icons/panel.png').convert_alpha()

# DEFINE GAME VARIABLES
current_dialog = 0
current_dialog_line = 0
current_bg = 0
dialog_lines = _('dialogs')

# function for drawing text in game window
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# function for drawing dialogs in panel
def blit_text(surface, text, pos, font, color=GRAY):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    word_width, word_height = 0, 0
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width - 20:
                x = pos[0]  # Reset the x.
                y += word_height + 5  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height + 5  # Start on new row.

# function for drawing selected dialog line
def draw_dialog(dialogs_list):
    if current_dialog < len(dialogs_list):
        if current_dialog_line < len(dialogs_list[current_dialog]):
            blit_text(screen, dialogs_list[current_dialog][current_dialog_line], (30, 620), font)
            pygame.draw.polygon(screen, GRAY, [(1225, 715),(1225, 725),(1235, 720)])
            pygame.draw.polygon(screen, GRAY, [(1240, 715),(1240, 725),(1250, 720)])
    else:
        raise IndexError("dialog index out of range")

# function for drawing background
def draw_bg():
    background = pygame.transform.scale(background_list[current_bg], (1280, 600))
    screen.blit(background, (0, 0))

# function for drawing interactions panel
def draw_panel():
    # draw panel rectangle
    panel = pygame.transform.scale(panel_img, (config.screen_width, config.bottom_panel))
    screen.blit(panel, (0, config.screen_height - config.bottom_panel))

def next_dialog():
    global current_dialog_line, current_dialog, current_bg
    current_dialog_line += 1
    if current_dialog_line == len(dialog_lines[current_dialog]):
        current_dialog_line = 0
        current_dialog += 1
        current_bg += 1
    print(current_dialog_line, current_dialog, current_bg)


# MAIN GAME LOOP
def run():
    global current_dialog, current_dialog_line, current_bg
    run = True
    read_locale_file(config.selected_lang or config.default_lang)
    dialog_lines = _('dialogs')

    while run:
        clock.tick(fps)

        # reset mouse click
        # clicked = False

        # draw background
        draw_bg()

        # draw panel
        draw_panel()

        draw_dialog(dialog_lines)

        # TODO: Add mouse support
        # mouse_pos = pygame.mouse.get_pos()
        # next_buttons = pygame.Rect((1225, 715),(25, 10))
        # if next_buttons.collidepoint(mouse_pos):
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        #     if clicked == True:
        #         next_dialog()
        # else:
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # if event.type == pygame.MOUSEBUTTONUP:
            #     clicked = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    next_dialog()

        pygame.display.update()

    pygame.quit()
