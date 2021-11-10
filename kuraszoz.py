#!/usr/bin/env python
import os
import random
import pygame
import time

pygame.init()

# Window config
WIDTH, HEIGHT = 1080, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KURAS ZoZ")
FPS = 60

# Colors and fonts
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("comicsans", 70, "bold")

# Configure game variables.
VEL = 5
SALAD_TRACKING_SPEED = 0.2
MAX_OBJECTS_AMOUNT = 5
VODKA_POINTS = 2
BEER_POINTS = 1
VODKA_HEAL = 2
BEER_HEAL = 1
MAX_HEALTH = 10
SALAD_DAMAGE = 5
CURRENT_HEALTH = 5

# Get scales
VODKA_WIDTH, VODKA_HEIGHT = (50, 200)
BEER_WIDTH, BEER_HEIGHT = (60, 150)
CHARACTER_WIDTH, CHARACTER_HEIGHT = (150, 150)
SALAD_WIDTH, SALAD_HEIGHT = (100, 60)

# Get sprites
BEER = pygame.image.load(os.path.join("sprites", "beer.png"))
VODKA = pygame.image.load(os.path.join("sprites", "vodka.png"))
BG = pygame.image.load(os.path.join("sprites", "fight.png"))
MAIN_CHARACTER = pygame.image.load(os.path.join("sprites", "kurasssigoj.png"))
SALAD = pygame.image.load(os.path.join("sprites", "salad.png"))

# Scale sprites
SALAD = pygame.transform.scale(SALAD, (SALAD_WIDTH, SALAD_HEIGHT))
BEER = pygame.transform.scale(BEER, (BEER_WIDTH, BEER_HEIGHT))
VODKA = pygame.transform.scale(VODKA, (VODKA_WIDTH, VODKA_HEIGHT))
MAIN_CHARACTER = pygame.transform.scale(MAIN_CHARACTER, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
BG = pygame.transform.scale(BG, (WIDTH,
                                 HEIGHT))


def draw_window(character, object_list, health_text, points_text):
    """Draw window."""
    WIN.blit(BG, (0, 0))
    character.draw_player()
    WIN.blit(health_text, (800, 40))
    WIN.blit(points_text, (40, 40))
    for element in object_list:
        element.draw_object()
    pygame.display.update()


def showGameOverScreen(keys_pressed, points):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    points_font = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render('Game Over', True, WHITE)
    overSurf = points_font.render(f'Your Points: {points}', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WIDTH / 2, 10)
    overRect.midtop = (WIDTH / 2, gameRect.height + 10 + 25)

    WIN.blit(gameSurf, gameRect)
    WIN.blit(overSurf, overRect)
    pygame.display.update()
    events = pygame.event.get()
    pygame.time.wait(2000)
    pygame.event.clear()


class Player:

    def __init__(self, x, y, health, width, height, run):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.points = 0
        self.image = MAIN_CHARACTER
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.run = run

    def draw_player(self):
        WIN.blit(self.image, self.rect)
        # pygame.draw.rect(WIN, (255, 255, 255), self.rect, 2)

    def move_player(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.rect.x - VEL > - 10:
            self.rect.x -= VEL
        if keys_pressed[pygame.K_d] and self.rect.x + VEL + self.width < 1100:
            self.rect.x += VEL

    def check_game_over(self, keys_pressed):
        if self.health <= 0:
            self.points += 50
            showGameOverScreen(keys_pressed, self.points)
            self.run = False


class FallingObjects:

    def __init__(self, x, y, object_type, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.object_type = object_type
        if object_type == "beer":
            self.image = BEER
        elif object_type == "vodka":
            self.image = VODKA
        elif object_type == "salad":
            self.image = SALAD
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_object(self):
        WIN.blit(self.image, self.rect)
        # pygame.draw.rect(WIN, (255, 255, 255), self.rect, 2)

    def fall(self, player_x):
        if self.object_type != "salad":
            self.rect.y += self.speed
        else:

            self.rect.y += self.speed

    def check_if_respawn(self):
        if self.rect.y > 900:
            self.rect.y = -200
            rand_x = random.randint(100, 1000)
            self.rect.x = rand_x

    def check_for_collisions(self, character):
        if self.rect.colliderect(character.rect):
            self.rect.y = -200
            rand_x = random.randint(100, 1000)
            self.rect.x = rand_x
            if self.object_type == "beer":
                if character.health <= MAX_HEALTH - BEER_HEAL:
                    character.health += 1
                character.points += 10
            elif self.object_type == "vodka":
                if character.health <= MAX_HEALTH - VODKA_HEAL:
                    character.health += 2
                character.points += 20
            elif self.object_type == "salad":
                character.health -= 5
                character.points -= 50
            print(character.health)


def main():
    run = True
    character = Player(500, 650, 5, CHARACTER_WIDTH, CHARACTER_HEIGHT, run)
    rand_x = random.randint(0, 1000)
    falling_beer1 = FallingObjects(rand_x, 0, "beer", 4)
    rand_x = random.randint(0, 1000)
    falling_beer2 = FallingObjects(rand_x, -200, "beer", 6)
    rand_x = random.randint(0, 1000)
    falling_vodka1 = FallingObjects(rand_x, -400, "vodka", 5)
    rand_x = random.randint(0, 1000)
    salad1 = FallingObjects(rand_x, -100, "salad", 4)
    rand_x = random.randint(0, 1000)
    salad2 = FallingObjects(rand_x, -700, "salad", 6)
    rand_x = random.randint(0, 1000)
    salad3 = FallingObjects(rand_x, -100, "salad", 7)
    object_list = [falling_vodka1, falling_beer1, salad1, falling_beer2, salad2, salad3]
    clock = pygame.time.Clock()
    while character.run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                character.run = False
                pygame.quit()


        keys_pressed = pygame.key.get_pressed()
        character.move_player(keys_pressed)
        points_text = FONT.render(f"Points: {character.points}", True, (0, 0, 0))
        health_text = FONT.render(f"Health: {character.health}", True, (0, 0, 0))
        draw_window(character, object_list, health_text, points_text)
        for element in object_list:
            element.fall(character.rect.x)
            element.check_if_respawn()
            element.check_for_collisions(character)
        character.check_game_over(keys_pressed)

    main()


if __name__ == '__main__':
    main()
