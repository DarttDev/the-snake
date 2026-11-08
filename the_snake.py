"""Главный модуль игры"""
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
START_SPEED = 5


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс"""

    def __init__(self) -> None:
        self.position: tuple = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color: tuple[int, int, int] = (0, 0, 0)

    def draw(self, game_screen: pygame.Surface,
             position: tuple[int, int]) -> None:
        """Отрисовывает ячеку на игровом поле"""
        rect: pygame.Rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(game_screen, self.body_color, rect)
        pygame.draw.rect(game_screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Отвечает за объект яблока в игре"""

    def __init__(self, snake_positions: list[tuple] | None = None) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions: list[tuple] | None) -> None:
        """Определяет случайную позицию яблока"""
        new_position = self._determine_new_position()

        if snake_positions is None:
            snake_positions = []

        while new_position in snake_positions:
            new_position = self._determine_new_position()

        self.position = new_position

    def _determine_new_position(self) -> tuple[int, int]:

        x: int = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y: int = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

        return (x, y)

    def draw_cell(self) -> None:
        """Отрисовывает яблоко на игровом поле"""
        self.draw(screen, self.position)


class Snake(GameObject):
    """Класс змейки на игровом поле"""

    def __init__(self) -> None:
        super().__init__()
        self.length: int
        self.direction: tuple[int, int]
        self.next_direction: None | tuple[int, int]
        self.body_color: tuple[int, int, int]
        self.last: None | tuple[int, int]
        self.positions: list[tuple]
        self.speed: float
        self.reset()

    def reset(self) -> None:
        """Обнуляет атрибуты змейки при проигрыше"""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.positions = [self.position]
        self.speed = START_SPEED

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def move(self) -> None:
        """Двигает змейку на игровом поле"""
        current_x, current_y = self.get_head_position()

        new_x = ((current_x + self.direction[0] * GRID_SIZE) %
                 (GRID_WIDTH * GRID_SIZE))

        new_y = ((current_y + self.direction[1] * GRID_SIZE) %
                 (GRID_HEIGHT * GRID_SIZE))

        new_head_position = (new_x, new_y)

        self.positions.insert(0, new_head_position)

        self.last = self.positions[-1]

        if len(self.positions) > self.length:
            del self.positions[-1]

    def update_direction(self) -> None:
        """Обновляет направление змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw_cell(self) -> None:
        """Отрисовывает змейку на игровом поле"""
        head_rect = self.get_head_position()
        self.draw(screen, head_rect)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object: Snake) -> None:
    """Обрабатывает действия пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Главный цикл игры"""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:

        clock.tick(snake.speed)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        snake_head_position = snake.get_head_position()

        if snake_head_position == apple.position:
            snake.length += 1
            snake.speed += 0.5
            apple.randomize_position(snake.positions)

        if snake_head_position in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw_cell()
        apple.draw_cell()

        pygame.display.update()


if __name__ == '__main__':
    main()
