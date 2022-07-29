'''
Author: Joe Auz
Version: 1.3.0
Name: ClickIn Ore
Summary: This is a game with heavy inspiration taken from Cookie Clicker. It is a simple incremental game,
you click the ore, you get ore. You currently have the option to purchase a miner to boost
the amount of ore you get per click. Are you able to reach the fabled Cobalt tier?
'''

from turtle import width
import pygame
import os
import json

pygame.display.set_caption('ClickIn Ore')
pygame.font.init()

# Global values
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 240
# ORES
ORE_WIDTH = 250
ORE_HEIGHT = 150
# MINER
MINER_WIDTH = 165
MINER_HEIGHT = 125
MINER_X = 10
MINER_Y = 550

# Events
MINER_SHOP = pygame.USEREVENT + 1

# Fonts
POINTS_FONT = pygame.font.SysFont('comicsans', 50)
CLICK_FONT = pygame.font.SysFont('comicsans', 35)
SHOP_FONT = pygame.font.SysFont('comicsans', 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Assets
MINE_BG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'background.png')), (WIDTH, HEIGHT))
COAL = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'coal.png')), (ORE_WIDTH, ORE_HEIGHT))
GOLD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'gold.png')), (ORE_WIDTH, ORE_HEIGHT))
TITANIUM = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'titanium.png')), (ORE_WIDTH, ORE_HEIGHT))
ADDY = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'adamantite.png')), (ORE_WIDTH, ORE_HEIGHT))
COBALT = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'cobalt.png')), (ORE_WIDTH, ORE_HEIGHT))
MINER = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'miner.png')), (MINER_WIDTH, MINER_HEIGHT))
PLAY_BTN = pygame.image.load(os.path.join('Assets', 'play_button.png'))
QUIT_BTN = pygame.image.load(os.path.join('Assets', 'quit_button.png'))


class Player:

    def __init__(self, total_ore, total_miners, miner_cost, miner_multiplier, ore_per_click):
        self.ore = total_ore
        self.miners = total_miners
        self.miner_cost = miner_cost
        self.per_click = ore_per_click
        self.multiplier = miner_multiplier

    def get_ore(self):
        return self.ore

    def get_per_click(self):
        return self.per_click

    def get_miners(self):
        return self.miners

    def get_mult(self):
        return self.multiplier

    def get_miner_cost(self):
        return self.miner_cost

    def inc_ore(self):
        self.ore += self.per_click

    def inc_miner(self):
        self.miners += 1
        self.ore -= self.miner_cost
        self.multiplier *= 1.005

    def up_miner_cost(self):
        self.miner_cost *= 1.25

    def up_per_click(self):
        self.per_click *= self.multiplier

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

def draw_play(player_one):
    WIN.blit(MINE_BG, (0, 0))

    if player_one.get_ore() < 10:
        WIN.blit(COAL, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))
    elif 10 <= player_one.get_ore() < 20:
        WIN.blit(GOLD, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))
    elif 20 <= player_one.get_ore() < 30:
        WIN.blit(TITANIUM, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))
    elif 30 <= player_one.get_ore() < 40:
        WIN.blit(ADDY, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))
    elif 40 <= player_one.get_ore():
        WIN.blit(COBALT, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))

    num_ore_text = POINTS_FONT.render(
        'Total Ore: ' + str(round(player_one.get_ore(), 2)), 1, WHITE)
    WIN.blit(num_ore_text, (WIDTH // 2 - ORE_WIDTH // 2, 10))

    ore_per_click_text = CLICK_FONT.render(
        'Per Click: ' + str(round(player_one.get_per_click(), 3)), 1, WHITE)
    WIN.blit(ore_per_click_text, (WIDTH // 2 - ORE_WIDTH // 2 + 30, 415))

    WIN.blit(MINER, (MINER_X, MINER_Y))

    miner_shop_count_text = SHOP_FONT.render(
        'Total Miners: ' + str(player_one.get_miners()), 1, WHITE)
    WIN.blit(miner_shop_count_text, (MINER_X + 15, MINER_Y - 25))

    miner_shop_cost_text = SHOP_FONT.render(
        'Cost: ' + str(round(player_one.get_miner_cost(), 2)), 1, WHITE)
    WIN.blit(miner_shop_cost_text, (MINER_X + 25, MINER_Y + 115))

    pygame.display.update()


def handle_miner_shop(player_one):
    if player_one.miners > 0:
        pygame.event.post(pygame.event.Event(MINER_SHOP))


def save_game(player_one):
    print(player_one.__dict__)
    with open('ClickIn_Ore.txt', 'w') as save_file:
        json.dump(player_one.__dict__, save_file)


def load_game():
    if os.path.exists('ClickIn_Ore.txt'):
        with open('ClickIn_Ore.txt') as save_file:
            loaded_data = json.load(save_file)
        return loaded_data
    else:
        return False


def menu():
    # WIN.blit(MINE_BG, (0, 0))
    play_btn = Button(100, 200, PLAY_BTN)
    quit_btn = Button(350, 200, QUIT_BTN)

    WIN.fill((202, 228, 241))
    menu_text = POINTS_FONT.render(
        'Main Menu', 1, WHITE)
    WIN.blit(menu_text, (WIDTH // 2 - ORE_WIDTH // 2, 10))
    play_btn.draw()
    quit_btn.draw()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if play_btn.rect.collidepoint(x, y):
                play()
            if quit_btn.rect.collidepoint(x, y):
                pygame.quit()

    pygame.display.update()


def play():

    if load_game():
        player_one = Player(load_game()['ore'], load_game()['miners'],
                            load_game()['miner_cost'], load_game()['multiplier'], load_game()['per_click'])

    else:
        player_one = Player(total_ore=0, total_miners=0,
                            miner_cost=5, miner_multiplier=1, ore_per_click=1)

    ore = pygame.Rect(WIDTH // 2 - ORE_WIDTH // 2, HEIGHT //
                      2 - 100, ORE_WIDTH, ORE_HEIGHT)
    miner = pygame.Rect(MINER_X, MINER_Y, MINER_WIDTH, MINER_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if ore.collidepoint(x, y):
                    player_one.inc_ore()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if miner.collidepoint(x, y) and player_one.ore >= player_one.miner_cost:
                    player_one.inc_miner()
                    handle_miner_shop(player_one)
            if event.type == MINER_SHOP:
                player_one.up_miner_cost()
                player_one.up_per_click()

        draw_play(player_one)
    save_game(player_one)
    pygame.quit()


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


if __name__ == '__main__':
    main()
