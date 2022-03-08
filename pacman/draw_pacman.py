import random
from abc import ABCMeta, abstractmethod

import pygame

from variables import (
    BLACK,
    BLUE,
    CYAN,
    DOWN,
    HEIGHT,
    LEFT,
    MAZE,
    ORANGE,
    PINK,
    RED,
    RIGHT,
    SPEED,
    UP,
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


class Movable(metaclass=ABCMeta):
    @abstractmethod
    def accept_movement(self):
        pass

    @abstractmethod
    def refuse_movement(self, directions):
        pass

    @abstractmethod
    def corner(self, directions):
        pass


class Scenery(GameElement):
    def __init__(self, size, pacman):
        self.pacman = pacman
        self.movables = []
        self.size = size
        self.points = 0
        self.matrix = MAZE
        self.state = "PLAYING"
        self.total_points = self.calculate_total_points()
        print(self.total_points)

    def calculate_total_points(self):
        points = 0
        for row in MAZE:
            points += row.count(1)
        return points

    def add_points(self):
        self.points += 1

    def add_movable(self, obj):
        self.movables.append(obj)

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
        if self.state == "PLAYING":
            self.paint_while_playing(screen)
        elif self.state == "PAUSED":
            self.paint_while_playing(screen)
            self.paint_while_paused(screen)
        elif self.state == "GAME_OVER":
            self.paint_while_playing(screen)
            self.paint_game_over(screen)
        elif self.state == "VICTORY":
            self.paint_while_playing(screen)
            self.paint_victory(screen)

    def paint_centered_text(self, screen, text, color):
        text_img = font.render(text, True, color, BLACK)
        text_x = (screen.get_width() - text_img.get_width()) // 2
        text_y = (screen.get_height() - text_img.get_height()) // 2
        screen.blit(text_img, (text_x, text_y))

    def paint_victory(self, screen):
        text = "Y O U  W I N !"
        self.paint_centered_text(screen, text, YELLOW)

    def paint_game_over(self, screen):
        text = "G A M E   O V E R"
        self.paint_centered_text(screen, text, RED)

    def paint_while_paused(self, screen):
        text = "P A U S E D"
        self.paint_centered_text(screen, text, YELLOW)

    def paint_while_playing(self, screen):
        for row_number, row in enumerate(self.matrix):
            self.paint_row(screen, row_number, row)
        self.paint_points(screen)

    def get_directions(self, row, column):
        directions = []
        if self.matrix[int(row - 1)][int(column)] != 2:
            directions.append(UP)
        if self.matrix[int(row + 1)][int(column)] != 2:
            directions.append(DOWN)
        if self.matrix[int(row)][int(column - 1)] != 2:
            directions.append(LEFT)
        if self.matrix[int(row)][int(column + 1)] != 2:
            directions.append(RIGHT)

        return directions

    def calculate_rules(self):
        if self.state == "PLAYING":
            self.calculate_rules_while_playing()
        elif self.state == "PAUSED":
            self.calculate_rules_while_paused()
        elif self.state == "GAME_OVER":
            self.calculate_rules_game_over()
        elif self.state == "VICTORY":
            self.calculate_rules_victory()

    def calculate_rules_victory(self):
        pass

    def calculate_rules_game_over(self):
        pass

    def calculate_rules_while_paused(self):
        pass

    def calculate_rules_while_playing(self):
        for element in self.movables:
            row = int(element.row)
            col = int(element.column)
            desired_mov_col = int(element.desired_mov_column)
            desired_mov_row = int(element.desired_mov_row)
            directions = self.get_directions(row, col)

            if len(directions) >= 3:
                element.corner(directions)

            if (
                isinstance(element, Ghost)
                and element.row == self.pacman.row
                and element.column == self.pacman.column
            ):
                self.state = "GAME_OVER"
            else:
                if (
                    0 <= desired_mov_row < 29
                    and 0 <= desired_mov_col < 28
                    and self.matrix[desired_mov_row][desired_mov_col] != 2
                ):
                    element.accept_movement()
                    if (
                        isinstance(element, Pacman)
                        and self.matrix[row][col] == 1
                    ):
                        self.add_points()
                        self.matrix[row][col] = 0

                        if self.points >= self.total_points:
                            self.state = "VICTORY"
                else:
                    element.refuse_movement(directions)

    def change_state(self):
        states = {"PLAYING": "PAUSED", "PAUSED": "PLAYING"}
        self.state = states.get(self.state)

    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.change_state()


class Pacman(GameElement, Movable):
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

    def refuse_movement(self, directions):
        self.desired_mov_row = self.row
        self.desired_mov_column = self.desired_mov_column

    def corner(self, directions):
        pass


class Ghost(GameElement):
    def __init__(self, size, color):
        self.column = 13
        self.row = 15
        self.speed = 1
        self.direction = 0
        self.size = size
        self.color = color
        self.desired_mov_column = self.column
        self.desired_mov_row = self.row

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
        if self.direction == UP:
            self.desired_mov_row -= self.speed
        elif self.direction == DOWN:
            self.desired_mov_row += self.speed
        elif self.direction == LEFT:
            self.desired_mov_column -= self.speed
        elif self.direction == RIGHT:
            self.desired_mov_column += self.speed

    def change_direction(self, directions):
        self.direction = random.choice(directions)

    def corner(self, directions):
        self.change_direction(directions)

    def accept_movement(self):
        self.row = self.desired_mov_row
        self.column = self.desired_mov_column

    def refuse_movement(self, directions):
        self.desired_mov_row = self.row
        self.desired_mov_column = self.column
        self.change_direction(directions)

    def process_events(self, events):
        pass


if __name__ == "__main__":
    size = HEIGHT // 30
    pacman = Pacman(size)
    blinky = Ghost(size, RED)
    inky = Ghost(size, CYAN)
    clyde = Ghost(size, ORANGE)
    pinky = Ghost(size, PINK)
    scenery = Scenery(size, pacman)
    scenery.add_movable(pacman)
    scenery.add_movable(blinky)
    scenery.add_movable(inky)
    scenery.add_movable(clyde)
    scenery.add_movable(pinky)

    while True:
        pacman.calculate_rules()
        blinky.calculate_rules()
        inky.calculate_rules()
        clyde.calculate_rules()
        pinky.calculate_rules()
        scenery.calculate_rules()

        screen.fill(BLACK)
        scenery.paint(screen)
        pacman.paint(screen)
        blinky.paint(screen)
        inky.paint(screen)
        clyde.paint(screen)
        pinky.paint(screen)

        pygame.display.update()
        pygame.time.delay(100)

        events = pygame.event.get()
        pacman.process_events(events)
        scenery.process_events(events)
