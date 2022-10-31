import pygame, sys
from pygame.locals import *
from src import game
from utils import config
from utils.helpers import t, read_locale_file

pygame.font.init()
font = pygame.font.SysFont(config.font_name, config.default_font_size)
small_font = pygame.font.SysFont(config.font_name, config.small_font_size)

logo = pygame.image.load("assets/img/Texts/logo.png")
bg = pygame.image.load("assets/img/Background/menu1.jpg")
bg = pygame.transform.scale(bg, (640, 375))

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 750))
display = pygame.Surface((640, 375))


def update_screen():
    screen.blit(pygame.transform.scale(display, (1280, 750)), (0, 0))
    pygame.display.update()
    clock.tick(24)
    last_frame = display.copy()


# pygame.mixer.init(44100, -16, 2, 512)
# pygame.mixer.music.load("music/Our-Mountain_v003_Looping-[Menu].mp3")


def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    if center:
        text_width = text_rect.topright[0] - text_rect.topleft[0]
        text_rect.topleft = (x - (text_width // 2), y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def blit_text(surface, text, pos, font, color=(156, 156, 156)):
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


def fade_out(screen, animIdx, function):
    radius = animIdx
    circle = pygame.draw.circle(screen, (0, 0, 0), (320, 200), radius)
    if animIdx == 420:
        function()


def init_menu_options():
    global menuOptions, optionsMenuOptions
    menuOptions = [
        t('main_menu.new_game'),
        t('main_menu.options'),
        t('main_menu.about'),
        t('main_menu.quit')
    ]
    optionsMenuOptions = [
        t('main_menu.language'),
        t('main_menu.difficulty'),
        t('main_menu.keys'),
        t('main_menu.back'),
    ]


init_menu_options()
menuIndex = 0
animIndex = 0
start = False


def main_menu(screen, gameFunction, updateFunction):
    global menuIndex, animIndex, start
    # pygame.mixer.music.play(-1)
    while True:
        # Menu Background -----------------#
        screen.blit(bg, (0, 0))

        # Game Logo ---------------------- #
        screen.blit(logo, (20, 10))

        # Menu Options ------------------- #
        for idx in range(len(menuOptions)):
            if idx == menuIndex:
                draw_text(menuOptions[idx], font, (255, 255, 255), screen, 20,
                          320 - (26 * (len(menuOptions) - idx - 1)))
            else:
                draw_text(menuOptions[idx], font, (150, 150, 150), screen, 20,
                          320 - (26 * (len(menuOptions) - idx - 1)))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if menuIndex > 0:
                        menuIndex -= 1
                if event.key == K_DOWN:
                    if menuIndex < len(menuOptions) - 1:
                        menuIndex += 1
                if event.key == K_RETURN:
                    if menuIndex == 0:
                        # pygame.mixer.music.fadeout(1000)
                        start = True
                    if menuIndex == 1:
                        options(screen, updateFunction)
                        menuIndex = 0
                    if menuIndex == 2:
                        about(screen, updateFunction)
                        menuIndex = 0
                    if menuIndex == 3:
                        pygame.quit()
                        sys.exit()

        if start and animIndex <= 420:
            fade_out(screen, animIndex, gameFunction)
            animIndex += 30
        updateFunction()


def options(screen, updateFunction):
    global menuIndex
    menuIndex = 0
    running = True
    while running:
        # Options Background -----------------#
        screen.blit(bg, (0, 0))

        # Game Logo ---------------------- #
        screen.blit(logo, (20, 10))

        # Title -------------------------- #
        draw_text(t('main_menu.options'), font, (255, 255, 255), screen, 320, 70, True)

        # Menu Options ------------------- #
        for idx in range(len(optionsMenuOptions)):
            if idx == menuIndex:
                draw_text(optionsMenuOptions[idx], font, (255, 255, 255), screen, 20,
                          320 - (26 * (len(optionsMenuOptions) - idx - 1)))
            else:
                draw_text(optionsMenuOptions[idx], font, (150, 150, 150), screen, 20,
                          320 - (26 * (len(optionsMenuOptions) - idx - 1)))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if menuIndex > 0:
                        menuIndex -= 1
                if event.key == K_DOWN:
                    if menuIndex < len(optionsMenuOptions) - 1:
                        menuIndex += 1
                if event.key == K_RETURN:
                    if menuIndex == 0:
                        change_lang(screen, updateFunction)
                    if menuIndex == 3:
                        running = False
        updateFunction()


def change_lang(screen, updateFunction):
    global menuIndex
    menuIndex = 0
    running = True
    while running:
        # Options Background -----------------#
        screen.blit(bg, (0, 0))

        # Game Logo ---------------------- #
        screen.blit(logo, (20, 10))

        # Title -------------------------- #
        draw_text(t('main_menu.language'), font, (255, 255, 255), screen, 320, 70, True)

        # Menu Options ------------------- #
        from os import walk

        filenames = next(walk('assets/lang'), (None, None, []))[2]
        langs = list(map(lambda el: el.split('.')[0], filenames))

        for idx, lang in enumerate(langs):
            if idx == menuIndex:
                draw_text(t(f'main_menu.lang.{lang}'), font, (255, 255, 255), screen, 20,
                          320 - (26 * (len(langs) - idx - 1)))
            else:
                draw_text(t(f'main_menu.lang.{lang}'), font, (150, 150, 150), screen, 20,
                          320 - (26 * (len(langs) - idx - 1)))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if menuIndex > 0:
                        menuIndex -= 1
                if event.key == K_DOWN:
                    if menuIndex < len(langs) - 1:
                        menuIndex += 1
                if event.key == K_RETURN:
                    if menuIndex == 0:
                        config.selected_lang = 'en'
                    if menuIndex == 1:
                        config.selected_lang = 'pl'
                    read_locale_file(config.selected_lang)
                    init_menu_options()
                    menuIndex = 0
                    running = False
        updateFunction()


def about(screen, updateFunction):
    global menuIndex
    menuIndex = 0
    running = True
    while running:
        # Options Background --------------#
        screen.blit(bg, (0, 0))

        # Game Logo ---------------------- #
        screen.blit(logo, (20, 10))

        # Title -------------------------- #
        draw_text(t('about.title'), font, (255, 255, 255), screen, 320, 70, True)
        # Menu Options ------------------- #
        draw_text(t('main_menu.back'), font, (255, 255, 255), screen, 20, 320)

        # Content ------------------------ #
        draw_text(f"{t('about.made')}:", small_font, (200, 200, 200), screen, 30, 100)
        draw_text("Jakub Michniewicz", small_font, (255, 255, 255), screen, 125, 100)

        draw_text(f"{t('about.scenario')}:", small_font, (200, 200, 200), screen, 30, 120)
        draw_text("Asia Wiewiórska", small_font, (255, 255, 255), screen, 125, 120)

        draw_text("\"Druga\"", font, (255, 255, 255), screen, 30, 150)
        about_text = t('about.description')
        blit_text(screen, about_text, (30, 175), small_font, (200, 200, 200))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if menuIndex == 0:
                        running = False
        updateFunction()


main_menu(display, game.run, update_screen)