import pygame

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WIDTH = 800
HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)


class Pacman:
    def __init__(self):
        self.column = 1
        self.row = 1
        self.center_x = 400
        self.center_y = 300
        self.size = WIDTH // 30
        self.speed_x = 1
        self.speed_y = 1

        self.radius = int(self.size / 2)

    def calculates_rules(self):
        self.column = self.column + self.speed_x
        self.row = self.row + self.speed_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.row * self.size + self.radius)

        if self.center_x + self.radius > WIDTH:
            self.speed_x = -1

        if self.center_x - self.radius < 0:
            self.speed_x = 1

        if self.center_y + self.radius > HEIGHT:
            self.speed_y = -1

        if self.center_y - self.radius < 0:
            self.speed_y = 1

    def paint(self, screen):
        if self.speed_x == -1:
            direction = -1
        else:
            direction = 1
        pygame.draw.circle(
            screen, YELLOW, (self.center_x, self.center_y), self.radius
        )
        mouth_corner = (self.center_x, self.center_y)
        upper_lip = (
            self.center_x + direction * self.radius,
            self.center_y - self.radius,
        )
        lower_lip = (self.center_x + direction * self.radius, self.center_y)
        points = [mouth_corner, upper_lip, lower_lip]
        pygame.draw.polygon(screen, BLACK, points, 0)

        eye = (
            int(self.center_x + self.radius / 3),
            int(self.center_y - self.radius * 0.70),
        )
        eye_radius = int(self.radius / 10)
        pygame.draw.circle(screen, BLACK, eye, eye_radius, 0)


if __name__ == "__main__":
    pacman = Pacman()

    while True:
        pacman.calculates_rules()
        screen.fill(BLACK)

        pacman.paint(screen)
        pygame.display.update()
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
