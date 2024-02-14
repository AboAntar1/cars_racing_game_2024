import random
import pygame
import time
import math
import os

# Set up the file paths
root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
font_path = os.path.join(
    root_dir, "../cars_racing_simple_game/fonts", "game_font.ttf")
collisionSound = os.path.join(
    root_dir, "../cars_racing_simple_game/sounds", "collision.mp3")
completeSound = os.path.join(
    root_dir, "../cars_racing_simple_game/sounds", "complete.wav")
petrolSound = os.path.join(
    root_dir, "../cars_racing_simple_game/sounds", "petrol.mp3")
gameOverSound = os.path.join(
    root_dir, "../cars_racing_simple_game/sounds", "game_over.wav")
grassImage = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "grass.jpg")
trackImage = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "track.png")
trackBorderImage = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "track-border.png")
finishImage = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "finish.png")
redCarImage = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "red-car.png")
greenCarImage = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "green-car.png")
greyCarImage = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "grey-car.png")
purpleCarImage = os.path.join(
    root_dir, "../cars_racing_simple_game/images", "purple-car.png")


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(
        render,
        (
            win.get_width() / 2 - render.get_width() / 2,
            win.get_height() / 2 - render.get_height() / 2,
        ),
    )


pygame.mixer.init()
pygame.font.init()

collision_sound = pygame.mixer.Sound(collisionSound)
level_complete_sound = pygame.mixer.Sound(completeSound)
petrol_sound = pygame.mixer.Sound(petrolSound)
game_over_sound = pygame.mixer.Sound(gameOverSound)

GRASS = pygame.image.load(grassImage)
TRACK = scale_image(pygame.image.load(trackImage), 0.9)

TRACK_BORDER = scale_image(pygame.image.load(trackBorderImage), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load(finishImage)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load(redCarImage), 0.55)
GREEN_CAR = scale_image(pygame.image.load(greenCarImage), 0.55)
GREY_CAR = scale_image(pygame.image.load(greyCarImage), 0.55)
PURPLE_CAR = scale_image(pygame.image.load(purpleCarImage), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cars Racing Simple Game 2024 [Easy Mode]")
MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 60
PATH = [
    (175, 119),
    (110, 70),
    (56, 133),
    (70, 481),
    (318, 731),
    (404, 680),
    (418, 521),
    (507, 475),
    (600, 551),
    (613, 715),
    (736, 713),
    (734, 399),
    (611, 357),
    (409, 343),
    (433, 257),
    (697, 258),
    (738, 123),
    (581, 71),
    (303, 78),
    (275, 377),
    (176, 388),
    (178, 260),
]


class GameInfo:
    LEVELS = 3  # Define the number of levels

    def __init__(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)


class AbstractCar:
    IMG = None  # Abstract class, IMG attribute should be defined in subclasses

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


CAR_IMAGES = [GREEN_CAR, GREY_CAR, PURPLE_CAR, RED_CAR]


class PlayerCar(AbstractCar):
    # Define the IMG attribute for the PlayerCar class
    IMG = None  # Default image, will be overridden during initialization

    START_POS = (180, 200)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        # Randomly select a car image path from the list
        self.img = random.choice(CAR_IMAGES)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0


def draw(win, images, player_car, computer_car, game_info):
    # Fill the window with a solid color (optional)
    win.fill((0, 0, 0))  # Black color

    # Blit the grass image onto the background, scaling it to fit the window
    grass_img = images[0][0]
    grass_rect = grass_img.get_rect()
    grass_img = pygame.transform.scale(
        grass_img, (win.get_width(), win.get_height()))
    grass_rect = grass_img.get_rect()
    win.blit(grass_img, grass_rect)

    # Blit other background images
    for img, pos in images[1:]:
        win.blit(img, pos)

    # Blit cars onto the game window
    player_car.draw(win)
    computer_car.draw(win)

    # Position the game data in the bottom left corner
    data_x = 20
    data_y = HEIGHT - 150

    # Define font style and size
    font = pygame.font.Font(None, 40)  # Adjust font size as needed
    bold_font = pygame.font.Font(None, 40)  # Font object for bold text
    bold_font.set_bold(True)  # Set the bold attribute to True

    level_data_text = bold_font.render(
        f"Level: {game_info.level}", 1, (255, 255, 255))
    win.blit(level_data_text, (data_x, data_y))

    time_data_text = bold_font.render(
        f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255)
    )
    win.blit(time_data_text, (data_x, data_y + 40))

    vel_data_text = bold_font.render(
        f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255)
    )
    win.blit(vel_data_text, (data_x, data_y + 80))

    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


collision_sound = pygame.mixer.Sound(collisionSound)
collision_volume = 0.2


def handle_collision(player_car, computer_car, game_info):
    global collision_volume
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.bounce()
        # Play collision sound with adjusted volume
        collision_sound.set_volume(collision_volume)
        collision_sound.play()  # Play collision sound
    computer_finish_poi_collide = computer_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide is not None:
        game_over_sound.play()
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    # Check collision with finish line for player car
    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide is not None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)
            level_complete_sound.play()

    # Boundary check to keep the player car within the screen
    if player_car.x < 0:
        player_car.x = 0
    elif player_car.x > WIDTH - player_car.img.get_width():
        player_car.x = WIDTH - player_car.img.get_width()

    if player_car.y < 0:
        player_car.y = 0
    elif player_car.y > HEIGHT - player_car.img.get_height():
        player_car.y = HEIGHT - player_car.img.get_height()


run = True
clock = pygame.time.Clock()
images = [
    (GRASS, (0, 0)),
    (TRACK, (0, 0)),
    (FINISH, FINISH_POSITION),
    (TRACK_BORDER, (0, 0)),
]
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(2, 4, PATH)
game_info = GameInfo()

current_volume = 0.0
volume_change_rate = 0.05

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car, game_info)

    while not game_info.started:
        blit_text_center(
            WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!"
        )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    petrol_sound.play(-1)
                game_info.start_level()

        if event.type == pygame.KEYUP and event.key == pygame.K_w:
            petrol_sound.stop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        petrol_sound.play(-1)
    else:
        petrol_sound.stop()

    if keys[pygame.K_w]:
        while current_volume < 1:
            current_volume += volume_change_rate
            if current_volume > 1:
                current_volume = 1
            petrol_sound.set_volume(current_volume)
    else:
        while current_volume > 0:
            current_volume -= volume_change_rate
            if current_volume < 0:
                current_volume = 0
            petrol_sound.set_volume(current_volume)

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car, game_info)

    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, "You won the game!")
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

pygame.quit()
