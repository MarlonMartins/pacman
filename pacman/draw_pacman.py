import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


class Pacman:
    def __init__(self):
        self.center_x = 400
        self.center_y = 300
        self.size = 100
        self.radius = int(self.size / 2)

    def paint(self, screen):

        pygame.draw.circle(
            screen, YELLOW, (self.center_x, self.center_y), self.radius
        )
        mouth_corner = (self.center_x, self.center_y)
        upper_lip = (self.center_x + self.radius, self.center_y - self.radius)
        lower_lip = (self.center_x + self.radius, self.center_y)
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

        pacman.paint(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
