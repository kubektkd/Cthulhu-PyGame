import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
bottom_panel = 150
screen_width = 1280
screen_height = 600 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Call of Cthulhu - Another one')

# define fonts
font = pygame.font.SysFont('Lucida Console', 18)

# define colours
red = (228, 27, 23)
green = (155, 227, 23)
gray = (156, 156, 156)

# load images
# background image
background_img = pygame.image.load('assets/img/Background/scene1.jpg').convert_alpha()
background_img2 = pygame.image.load('assets/img/Background/scene2.jpg').convert_alpha()
background_list = [background_img, background_img2]
logo_img = pygame.image.load('assets/img/Texts/logo.png').convert_alpha()
# panel image
panel_img = pygame.image.load('assets/img/Icons/panel.png').convert_alpha()
# button images

# define game variables
current_dialog = 0

# create a function for drawing text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def blit_text(surface, text, pos, font, color=gray):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
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

def draw_dialog(dialogs_list):
    if current_dialog < len(dialogs_list):
        blit_text(screen, dialogs_list[current_dialog], (30, 620), font)
        pygame.draw.polygon(screen, gray, [(1225, 715),(1225, 725),(1235, 720)])
        pygame.draw.polygon(screen, gray, [(1240, 715),(1240, 725),(1250, 720)])

# function for drawing background
def draw_bg():
    background = pygame.transform.scale(background_list[current_dialog], (1280, 600))
    logo = pygame.transform.scale(logo_img, (150, 50))
    screen.blit(background, (0, 0))
    screen.blit(logo_img, (20, 540))

# function for drawing panel
def draw_panel():
    # draw panel rectangle
    panel = pygame.transform.scale(panel_img, (1280, 150))
    screen.blit(panel, (0, screen_height - bottom_panel))
    # # show knight stats
    # draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    # for count, i in enumerate(bandit_list):
    #     # show name and health
    #     draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)

text_list = [
    'Stoksj?? to licz??ce zaledwie 2 tysi??ce mieszka??c??w miasteczko po??o??one w centrum prowincji o nazwie Helbjerg, w kt??rym pe??nisz rol?? komendanta ma??ego posterunku policji.',
    'Jest 12 lutego 2020 r. - Wracasz p????n?? noc?? radiowozem z oddalonego o przesz??o 80 km miasta, w kt??rym sk??ada??e?? przed s??dem zeznania dotycz??ce jednej z Twoich ostatnich spraw. \nW??ska droga do domu, biegn??ca dnem kotliny i wci??ni??ta pomi??dzy dwa poro??ni??te ciemnym lasem wzg??rza, pokryta jest ??wie??ym ??niegiem.',
    'Niespodziewanie, wyje??d??aj??c zza zakr??tu, dostrzegasz w ??wiat??ach swojego samochodu sylwetk?? dziewczyny. S??aniaj??c si?? boso poboczem w kierunku miasta, prawdopodobnie za chwil?? wejdzie pod ko??a Twojego radiowozu.'
]

text_list_en = [
    'Stoksj?? is a town with only 2,000 inhabitants in the center of the province of Helbjerg, where you are the commander of a small police station.',
    'It is February 12, 2020 - You are returning late at night in a police car from a city over 80 km away, in which you gave a testimony to the court regarding one of your last cases.\nThe narrow road to the house, running along the bottom of the valley and squeezed between two dark forest covered hills, is covered with fresh snow.',
    'Unexpectedly, as you drive around the bend, you see the silhouette of a girl in the headlights of your car. Staggering barefoot along the road towards the city, he will probably come under the wheels of your police car in a moment.'
]


def run():
    global current_dialog
    run = True

    while run:
        clock.tick(fps)

        # draw background
        draw_bg()

        # draw panel
        draw_panel()

        draw_dialog(text_list_en)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    current_dialog += 1

        pygame.display.update()

    pygame.quit()