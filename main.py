import pygame
import os

pygame.display.set_caption('--Game Title Here--')
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


def draw_window(total_ore, total_miners, miner_cost, ore_per_click):
    WIN.blit(MINE_BG, (0, 0))

    if total_ore < 10:
        WIN.blit(COAL, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))
    elif 10 <= total_ore < 20:
        WIN.blit(GOLD, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))
    elif 20 <= total_ore < 30:
        WIN.blit(TITANIUM, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))
    elif 30 <= total_ore < 40:
        WIN.blit(ADDY, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))
    elif 40 <= total_ore:
        WIN.blit(COBALT, (WIDTH//2 - ORE_WIDTH // 2, HEIGHT // 2 - 100))

    num_ore_text = POINTS_FONT.render('Total Ore: ' + str(round(total_ore, 2)), 1, WHITE)
    WIN.blit(num_ore_text, (WIDTH // 2 - ORE_WIDTH // 2, 10))

    ore_per_click_text = CLICK_FONT.render('Per Click: ' + str(round(ore_per_click, 2)), 1, WHITE)
    WIN.blit(ore_per_click_text, (WIDTH // 2 - ORE_WIDTH //2 + 30, 415))

    WIN.blit(MINER, (MINER_X, MINER_Y))

    miner_shop_count_text = SHOP_FONT.render(
        'Total Miners: ' + str(total_miners), 1, WHITE)
    WIN.blit(miner_shop_count_text, (MINER_X + 15, MINER_Y - 25))

    miner_shop_cost_text = SHOP_FONT.render('Cost: '+ str(round(miner_cost, 2)), 1, WHITE)
    WIN.blit(miner_shop_cost_text, (MINER_X+ 25, MINER_Y + 115))
    
    pygame.display.update()


def handle_miner_shop(total_miners):
    if total_miners > 0:
        pygame.event.post(pygame.event.Event(MINER_SHOP))


def main():
    ore = pygame.Rect(WIDTH // 2 - ORE_WIDTH // 2, HEIGHT //
                      2 - 100, ORE_WIDTH, ORE_HEIGHT)
    miner = pygame.Rect(MINER_X, MINER_Y, MINER_WIDTH, MINER_HEIGHT)

    ore_per_click = 1
    total_ore = 0
    total_miners = 0
    miner_multiplier = 1
    miner_cost = 5

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
                    total_ore += ore_per_click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if miner.collidepoint(x, y) and total_ore >= miner_cost:
                    total_ore -= miner_cost
                    total_miners += 1
                    handle_miner_shop(total_miners)
            if event.type == MINER_SHOP:
                miner_multiplier += 0.1
                miner_cost = miner_cost * miner_multiplier
                ore_per_click = ore_per_click * miner_multiplier


        draw_window(total_ore, total_miners, miner_cost, ore_per_click)

    pygame.quit()


if __name__ == '__main__':
    main()
