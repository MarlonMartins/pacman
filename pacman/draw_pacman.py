from abc import ABCMeta, abstractmethod

import pygame

from variables import (
    BLACK,
    BLUE,
    HEIGHT,
    MAZE,
    RED,
    SPEED,
    WHITE,
    WIDTH,
    YELLOW,
)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)

font = pygame.font.SysFont("arial", 32, True, False)


class GameElement(metaclass=ABCMeta):
    @abstractmethod
    def paint(self, screen):
        pass

    @abstractmethod
    def calculate_rules(self):
        pass

    @abstractmethod
    def process_events(self, events):
        pass


class Scenery(GameElement):
    def __init__(self, size, pacman):
        self.pacman = pacman
        self.size = size
        self.points = 0
        self.matrix = MAZE

    def check_color(self, column):
        if column == 2:
            return BLUE
        return BLACK

    def paint_points(self, screen):
        points_x = 30 * self.size
        img_points = font.render(f"Score: {self.points}", True, YELLOW)
        screen.blit(img_points, (points_x, 50))

    def paint_row(self, screen, row_number, row):
        for column_number, column in enumerate(row):
            x = column_number * self.size
            y = row_number * self.size
            food_radius = self.size // 10
            half = self.size // 2

            color = self.check_color(column)

            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)

            if column == 1:
                pygame.draw.circle(
                    screen, YELLOW, (x + half, y + half), food_radius, 0
                )

    def paint(self, screen):
        for row_number, row in enumerate(self.matrix):
            self.paint_row(screen, row_number, row)
        self.paint_points(screen)

    def calculate_rules(self):
        column = self.pacman.desired_mov_column
        row = self.pacman.desired_mov_row

        if 0 <= column <= 27 and 0 <= row < 29:
            if self.matrix[row][column] != 2:
                self.pacman.accept_movement()
                if self.matrix[row][column] == 1:
                    self.points += 1
                    self.matrix[row][column] = 0

    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                exit()


class Pacman(GameElement):
    def __init__(self, size):
        self.column = 1
        self.row = 1
        self.center_x = 400
        self.center_y = 300
        self.size = size
        self.speed_x = 0
        self.speed_y = 0
        self.radius = int(self.size / 2)
        self.desired_mov_column = self.column
        self.desired_mov_row = self.row

    def calculate_rules(self):
        self.desired_mov_column = self.column + self.speed_x
        self.desired_mov_row = self.row + self.speed_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.row * self.size + self.radius)

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
        eye_radius = int(self.radius / 8)
        pygame.draw.circle(screen, BLACK, eye, eye_radius, 0)

    def process_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.speed_x = SPEED
                    self.speed_y = 0
                elif event.key == pygame.K_LEFT:
                    self.speed_x = -SPEED
                    self.speed_y = 0
                elif event.key == pygame.K_UP:
                    self.speed_y = -SPEED
                    self.speed_x = 0
                elif event.key == pygame.K_DOWN:
                    self.speed_y = SPEED
                    self.speed_x = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.speed_x = 0
                elif event.key == pygame.K_LEFT:
                    self.speed_x = 0
                elif event.key == pygame.K_UP:
                    self.speed_y = 0
                elif event.key == pygame.K_DOWN:
                    self.speed_y = 0

    def accept_movement(self):
        self.row = self.desired_mov_row
        self.column = self.desired_mov_column


class Ghost(GameElement):
    def __init__(self, size, color):
        self.column = 6.0
        self.row = 8.0
        self.size = size
        self.color = color

    def paint(self, screen):
        slice = self.size // 8
        px = int(self.column * self.size)
        py = int(self.row * self.size)
        contour = [
            (px, py + self.size),
            (px + slice, py + slice * 2),
            (px + slice * 2, py + slice // 2),
            (px + slice * 3, py),
            (px + slice * 5, py),
            (px + slice * 6, py + slice // 2),
            (px + slice * 7, py + slice * 2),
            (px + self.size, py + self.size),
        ]
        pygame.draw.polygon(screen, self.color, contour, 0)

        eye_radius_ext = slice
        eye_radius_int = slice // 2

        eye_left_x = int(px + slice * 2.5)
        eye_left_y = int(py + slice * 2.5)

        eye_right_x = int(px + slice * 5.5)
        eye_right_y = int(py + slice * 2.5)

        pygame.draw.circle(
            screen, WHITE, (eye_left_x, eye_left_y), eye_radius_ext, 0
        )
        pygame.draw.circle(
            screen, BLACK, (eye_left_x, eye_left_y), eye_radius_int, 0
        )

        pygame.draw.circle(
            screen, WHITE, (eye_right_x, eye_right_y), eye_radius_ext, 0
        )
        pygame.draw.circle(
            screen, BLACK, (eye_right_x, eye_right_y), eye_radius_int, 0
        )

    def calculate_rules(self):
        pass

    def process_events(self, events):
        pass


if __name__ == "__main__":
    size = HEIGHT // 30
    pacman = Pacman(size)
    blinky = Ghost(size, RED)
    scenery = Scenery(size, pacman)

    while True:
        pacman.calculate_rules()
        scenery.calculate_rules()
        screen.fill(BLACK)
        scenery.paint(screen)
        pacman.paint(screen)
        blinky.paint(screen)
        pygame.display.update()
        pygame.time.delay(100)

        events = pygame.event.get()
        pacman.process_events(events)
        scenery.process_events(events)
