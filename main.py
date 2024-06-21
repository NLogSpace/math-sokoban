import pygame
import sys
from dataclasses import dataclass
from typing import Tuple
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rectangle Drawing Example")

# Set up the font and size
font_size = 36
font = pygame.font.Font(None, font_size)  # Default font

@dataclass
class Tile:
    type: str
    color: Tuple[int, int, int]

tile_size = 40
width = 20
height = 15 
speed = 0.1

def make_tile(type):
    if type == "floor":
        brightness = random.randint(70, 80)
        tile_color = (brightness, brightness, brightness)
        tile = Tile("floor", tile_color)
        return tile
    if type == "wall":
        r = random.randint(140, 160)
        g = random.randint(30, 40)
        b = random.randint(40, 50)
        tile_color = (r, g, b)
        tile = Tile("wall", tile_color)
        return tile

field = [[None for _ in range(height)] for _ in range(width)]
for x in range(width):
    for y in range(height):
        if x == 0 or y == 0 or x == width-1 or y == height-1:
            field[x][y] = make_tile("wall")
        else:
            field[x][y] = make_tile("floor")
for x in range(width-4, width):
    field[x][6] = make_tile("wall")
    field[x][8] = make_tile("wall")


@dataclass
class Float2:
    x: float
    y: float

    def __add__(self, other):
        return Float2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return Float2(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Float2({self.x}, {self.y})"

@dataclass
class Int2:
    x: int
    y: int

    def __add__(self, other):
        return Int2(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Int2({self.x}, {self.y})"

    def to_float(self):
        return Float2(self.x, self.y)

@dataclass
class Actor:
    type: str
    color: Tuple[int, int, int]
    pos: Float2
    direction: Float2
    tile_pos: Int2
    progress: float
    moving: bool
    char: str

player = Actor(
        type="player",
        color=(255, 215, 0),
        pos=Float2(5.0, 5.0),
        direction=None,
        tile_pos=Int2(5, 5),
        progress=0.0,
        moving=False,
        char="P")

actors = [player]
calc = "82-4!+3"
for i, char in enumerate(calc):
    r = random.randint(100, 160)
    g = random.randint(200, 240)
    b = random.randint(160, 200)
    box = Actor(type="box",
                color=(r, g, b),
                pos=Float2(float(2*i+3), 10),
                direction=None,
                tile_pos=Int2(2*i+3, 10),
                progress=0.0,
                moving=False,
                char=char)
    actors.append(box)



# Set up the clock for managing frame rate
clock = pygame.time.Clock()

directions = {"up": Int2(0, -1), "right": Int2(1, 0), "down": Int2(0, 1), "left": Int2(-1, 0)}

def is_in_bounds(tile_pos):
    return tile_pos.x >= 0 and tile_pos.x < width and tile_pos.y >= 0 and tile_pos.y < height

def init_move(direction):
    if player.moving:
        return
    dir_vector = directions[direction]
    current_pos = player.tile_pos
    actors_to_move = [player]
    done = False
    blocked = False
    while not done:
        done = True
        current_pos += dir_vector
        if not is_in_bounds(current_pos):
            blocked = True
            return
        if field[current_pos.x][current_pos.y].type == "wall":
            blocked = True
            return
        for actor in actors:
            if actor.tile_pos == current_pos:
                done = False
                actors_to_move.append(actor)

    for actor in actors_to_move:
        actor.tile_pos += dir_vector
        actor.direction = dir_vector.to_float()
        actor.progress = 0.0
        actor.moving=True



def update():
    # Continue movement
    for actor in actors:
        if actor.moving:
            actor.pos += actor.direction * speed
            actor.progress += speed
            if actor.progress >= 1:
                actor.moving = False
                actor.pos.x = float(actor.tile_pos.x)
                actor.pos.y = float(actor.tile_pos.y)

    if not player.moving:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:  # Up arrow key
            init_move("up")
        if keys[pygame.K_DOWN]:  # Down arrow key
            init_move("down")
        if keys[pygame.K_LEFT]:  # Left arrow key
            init_move("left")
        if keys[pygame.K_RIGHT]:  # Right arrow key
            init_move("right")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw field
    for x in range(width):
        for y in range(height):
            pygame.draw.rect(screen, field[x][y].color, (x*tile_size, y*tile_size, tile_size, tile_size))

    # Draw actors 
    for actor in actors:
        pygame.draw.rect(screen, actor.color, (actor.pos.x*tile_size, actor.pos.y*tile_size, tile_size, tile_size))
        text_surface = font.render(actor.char, True, (0, 0, 0))  # 'True' for anti-aliased text
        screen.blit(text_surface, (actor.pos.x*tile_size + (tile_size - text_surface.get_width())/2, actor.pos.y*tile_size + (tile_size - text_surface.get_height())/2))
    
    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

# Quit Pygame when the game loop ends
pygame.quit()
sys.exit()

