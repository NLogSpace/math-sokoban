import pygame
import sys
from dataclasses import dataclass
from typing import Tuple
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_SIZE = 36
TILE_SIZE = 40
FIELD_WIDTH = 20
FIELD_HEIGHT = 15
SPEED = 0.1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rectangle Drawing Example")

# Set up the font
font = pygame.font.Font(None, FONT_SIZE)  # Default font

@dataclass
class Float2:
    x: float
    y: float

    def __add__(self, other):
        return Float2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return Float2(self.x * scalar, self.y * scalar)

@dataclass
class Int2:
    x: int
    y: int

    def __add__(self, other):
        return Int2(self.x + other.x, self.y + other.y)

    def to_float(self):
        return Float2(self.x, self.y)

@dataclass
class Tile:
    type: str
    color: Tuple[int, int, int]

@dataclass
class Actor:
    type: str
    color: Tuple[int, int, int]
    pos: Float2
    direction: Float2 = None
    tile_pos: Int2 = None
    progress: float = 0.0
    moving: bool = False
    char: str = ''

def make_tile(type: str) -> Tile:
    if type == "floor":
        brightness = random.randint(70, 80)
        return Tile(type, (brightness, brightness, brightness))
    elif type == "wall":
        r = random.randint(140, 160)
        g = random.randint(30, 40)
        b = random.randint(40, 50)
        return Tile(type, (r, g, b))

def initialize_field(width: int, height: int):
    field = [[None for _ in range(height)] for _ in range(width)]
    for x in range(width):
        for y in range(height):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                field[x][y] = make_tile("wall")
            else:
                field[x][y] = make_tile("floor")
    for x in range(width - 4, width):
        field[x][6] = make_tile("wall")
        field[x][8] = make_tile("wall")
    return field

field = initialize_field(FIELD_WIDTH, FIELD_HEIGHT)

player = Actor(
    type="player",
    color=(255, 215, 0),
    pos=Float2(5.0, 5.0),
    tile_pos=Int2(5, 5),
    char="P"
)

actors = [player]
calc = "82-4!+3"
for i, char in enumerate(calc):
    r = random.randint(100, 160)
    g = random.randint(200, 240)
    b = random.randint(160, 200)
    box = Actor(
        type="box",
        color=(r, g, b),
        pos=Float2(float(2 * i + 3), 10),
        tile_pos=Int2(2 * i + 3, 10),
        char=char
    )
    actors.append(box)

clock = pygame.time.Clock()

directions = {
    "up": Int2(0, -1),
    "right": Int2(1, 0),
    "down": Int2(0, 1),
    "left": Int2(-1, 0)
}

def is_in_bounds(tile_pos: Int2) -> bool:
    return 0 <= tile_pos.x < FIELD_WIDTH and 0 <= tile_pos.y < FIELD_HEIGHT

def init_move(direction: str):
    if player.moving:
        return
    dir_vector = directions[direction]
    current_pos = player.tile_pos
    actors_to_move = [player]
    blocked = False

    while True:
        current_pos += dir_vector
        if not is_in_bounds(current_pos) or field[current_pos.x][current_pos.y].type == "wall":
            blocked = True
            break
        for actor in actors:
            if actor.tile_pos == current_pos:
                actors_to_move.append(actor)
                break
        else:
            break

    if not blocked:
        for actor in actors_to_move:
            actor.tile_pos += dir_vector
            actor.direction = dir_vector.to_float()
            actor.progress = 0.0
            actor.moving = True

def handle_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def update():
    for actor in actors:
        if actor.moving:
            actor.pos += actor.direction * SPEED
            actor.progress += SPEED
            if actor.progress >= 1:
                actor.moving = False
                actor.pos = actor.tile_pos.to_float()

    if not player.moving:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            init_move("up")
        if keys[pygame.K_DOWN]:
            init_move("down")
        if keys[pygame.K_LEFT]:
            init_move("left")
        if keys[pygame.K_RIGHT]:
            init_move("right")

def draw_field():
    for x in range(FIELD_WIDTH):
        for y in range(FIELD_HEIGHT):
            pygame.draw.rect(screen, field[x][y].color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_actors():
    for actor in actors:
        pygame.draw.rect(screen, actor.color, (actor.pos.x * TILE_SIZE, actor.pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        text_surface = font.render(actor.char, True, BLACK)
        screen.blit(text_surface, (
            actor.pos.x * TILE_SIZE + (TILE_SIZE - text_surface.get_width()) / 2,
            actor.pos.y * TILE_SIZE + (TILE_SIZE - text_surface.get_height()) / 2
        ))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            handle_event(event)

        update()

        screen.fill(WHITE)
        draw_field()
        draw_actors()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

