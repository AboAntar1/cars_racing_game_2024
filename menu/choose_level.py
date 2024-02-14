import pygame
import os
import sys
import random

# Define constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 80
BUTTON_SPACING = 40
FONT_SIZE = 40
TITLE_FONT_SIZE = 55
SCALE_OFFSET_X = 15
SCALE_OFFSET_Y = 5

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
button_click_sound = os.path.join(
    root_dir, "../cars_racing_simple_game/sounds", "button_click_sound.wav")
background_image_path = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "start_background_image.jpg")
font_path = os.path.join(
    root_dir, "../cars_racing_simple_game/fonts", "game_font.ttf")
button_container_path = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "button_container.png")
stars = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "stars.png")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to open the game modes


def open_game(mode):
    os.system(mode)

# Class for bubbles


class Bubble:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.image = pygame.image.load(os.path.join(
            root_dir, stars))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.window_width)
        self.rect.y = random.randint(-100, 0)
        self.speed = random.randint(1, 2)  # Adjusted speed for slower movement

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.window_height:
            self.rect.y = random.randint(-100, 0)
            self.rect.x = random.randint(0, self.window_width)
            # Adjusted speed for slower movement
            self.speed = random.randint(1, 2)

    def draw(self, window):
        window.blit(self.image, self.rect)


# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Cars Racing Simple Game 2024")

# Load background image
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(
    background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load custom font for the buttons
font = pygame.font.Font(font_path, FONT_SIZE)

# Load title font
title_font = pygame.font.Font(font_path, TITLE_FONT_SIZE)

# Load button container image for each button
button_container = pygame.image.load(button_container_path)
button_container = pygame.transform.scale(
    button_container, (BUTTON_WIDTH, BUTTON_HEIGHT))

# Create Rect objects for the containers
easy_container_rect = button_container.get_rect()
easy_container_rect.topleft = ((WINDOW_WIDTH - BUTTON_WIDTH) // 2,
                               (WINDOW_HEIGHT - (3 * (BUTTON_HEIGHT + BUTTON_SPACING))) // 2)
medium_container_rect = easy_container_rect.move(
    0, BUTTON_HEIGHT + BUTTON_SPACING)
hard_container_rect = medium_container_rect.move(
    0, BUTTON_HEIGHT + BUTTON_SPACING)

# Create a list to hold bubble objects
bubbles = [Bubble(WINDOW_WIDTH, WINDOW_HEIGHT)
           for _ in range(5)]  # Adjusted the number of bubbles

# Define paths for game modes
easy_mode = os.path.join(
    root_dir, "../cars_racing_simple_game/levels", "easy.py")
medium_mode = os.path.join(
    root_dir, "../cars_racing_simple_game/levels", "medium.py")
hard_mode = os.path.join(
    root_dir, "../cars_racing_simple_game/levels", "hard.py")

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if easy_container_rect.collidepoint(mouse_pos):
                open_game(easy_mode)
                pygame.mixer.Sound(button_click_sound).play()
            elif medium_container_rect.collidepoint(mouse_pos):
                open_game(medium_mode)
                pygame.mixer.Sound(button_click_sound).play()
            elif hard_container_rect.collidepoint(mouse_pos):
                open_game(hard_mode)
                pygame.mixer.Sound(button_click_sound).play()

    # Clear the screen
    window.fill(BLACK)

    # Draw background
    window.blit(background_image, (0, 0))

    # Draw bubbles
    for bubble in bubbles:
        bubble.update()
        bubble.draw(window)

    # Draw title
    title_text = title_font.render("Choose Playing Mode", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    window.blit(title_text, title_rect)

    # Draw buttons with scaling effect on hover
    for container_rect in [easy_container_rect, medium_container_rect, hard_container_rect]:
        if container_rect.collidepoint(pygame.mouse.get_pos()):
            scaled_button = pygame.transform.scale(
                button_container, (int(BUTTON_WIDTH * 1.1), int(BUTTON_HEIGHT * 1.1)))
            window.blit(scaled_button, (container_rect.x -
                        SCALE_OFFSET_X, container_rect.y - SCALE_OFFSET_Y))
        else:
            window.blit(button_container, container_rect)

    # Draw button labels
    easy_text = font.render("Easy", True, WHITE)
    window.blit(easy_text, (easy_container_rect.centerx - easy_text.get_width() //
                2, easy_container_rect.centery - easy_text.get_height() // 2))

    medium_text = font.render("Medium", True, WHITE)
    window.blit(medium_text, (medium_container_rect.centerx - medium_text.get_width() //
                2, medium_container_rect.centery - medium_text.get_height() // 2))

    hard_text = font.render("Hard", True, WHITE)
    window.blit(hard_text, (hard_container_rect.centerx - hard_text.get_width() //
                2, hard_container_rect.centery - hard_text.get_height() // 2))

    # Update the display
    pygame.display.flip()

# Quit Pygame outside the game loop
pygame.quit()
sys.exit()
