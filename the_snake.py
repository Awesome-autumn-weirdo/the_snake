import pygame
from random import randint

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость игры
SPEED = 20

# Глобальные переменные для экрана и времени
screen = None
clock = None


class GameObject:
    """Класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        super().__init__(
            position=self.randomize_position(),
            body_color=APPLE_COLOR
        )

    def randomize_position(self):
        """Случайно выбирает новую позицию для яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__(
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=SNAKE_COLOR
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в направлении."""
        head_x, head_y = self.positions[0]
        new_head = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE
        )

        # Проверка выхода за границы экрана
        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )

        # Добавляем новую позицию головы
        self.positions.insert(0, new_head)

        # Проверяем, нужно ли увеличить длину
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.next_direction = UP
    elif keys[pygame.K_DOWN]:
        snake.next_direction = DOWN
    elif keys[pygame.K_LEFT]:
        snake.next_direction = LEFT
    elif keys[pygame.K_RIGHT]:
        snake.next_direction = RIGHT


def main():
    """Главная функция игры."""
    global screen, clock
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Проверка типов screen и clock
    assert isinstance(screen, pygame.Surface),
    assert isinstance(clock, pygame.time.Clock),

    # Создание объектов
    snake = Snake()
    apple = Apple()

    # Игровой цикл
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Обработка клавиш
        handle_keys(snake)

        # Обновление состояния змейки
        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        # Проверка столкновения змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Отрисовка объектов
        snake.draw(screen)
        apple.draw(screen)

        # Обновление экрана
        pygame.display.update()

        # Задержка для регулировки скорости
        clock.tick(10)


if __name__ == '__main__':
    main()
