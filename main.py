import pygame
import random

# تنظیمات بازی
WIDTH = 800
HEIGHT = 600
FPS = 10
GRID_SIZE = 20

# تعریف رنگ‌ها
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# تنظیمات قلم
FONT_NAME = pygame.font.match_font('arial')

# تعریف کلاس مار
class Snake:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.dx = GRID_SIZE
        self.dy = 0
        self.body = [(self.x, self.y)]
        self.length = 1

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.body.append((self.x, self.y))
        if len(self.body) > self.length:
            del self.body[0]

    def change_direction(self, dx, dy):
        self.dx = dx * GRID_SIZE
        self.dy = dy * GRID_SIZE

    def draw(self, surface):
        for x, y in self.body:
            pygame.draw.rect(surface, GREEN, (x, y, GRID_SIZE, GRID_SIZE))

# تابع اصلی
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = (random.randint(0, WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE,
             random.randint(0, HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE)

    score = 0
    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(1, 0)
                elif event.key == pygame.K_UP:
                    snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, 1)

        if not game_over:
            snake.move()

            # بررسی برخورد با دیوارهای صفحه
            if snake.x < 0 or snake.x >= WIDTH or snake.y < 0 or snake.y >= HEIGHT:
                game_over = True

            # بررسی خوردن سیب
            if snake.x == apple[0] and snake.y == apple[1]:
                snake.length += 1
                score += 10
                apple = (random.randint(0, WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE,
                         random.randint(0, HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE)

            # بررسی برخورد با خود مار
            if (snake.x, snake.y) in snake.body[:-1]:
                game_over = True

            # نمایش اجزاء بازی در صفحه
            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, (apple[0], apple[1], GRID_SIZE, GRID_SIZE))
            snake.draw(screen)

        # نمایش امتیاز
        draw_text(screen, 'Score: ' + str(score), 18, WIDTH // 2, 10)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# تابع نمایش متن
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# اجرای بازی
game_loop()