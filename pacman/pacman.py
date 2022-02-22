import pygame

pygame.init()

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SPEED = 1
RADIUS = 30
screen = pygame.display.set_mode((640, 480), 0)
x = 10
y = 10
speed_x = SPEED
speed_y = SPEED

while True:

    x += speed_x
    y += speed_y

    if (x + RADIUS) > 640:
        speed_x = -SPEED

    if (x - RADIUS) < 0:
        speed_x = SPEED

    if (y + RADIUS) > 480:
        speed_y = -SPEED

    if (y - RADIUS) < 0:
        speed_y = SPEED

    screen.fill(BLACK)
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), RADIUS, 0)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
