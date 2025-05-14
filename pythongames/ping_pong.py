import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
PADDLE_SPEED = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move_up(self):
        self.rect.y -= PADDLE_SPEED
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += PADDLE_SPEED
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = random.choice((BALL_SPEED_X, -BALL_SPEED_X))
        self.speed_y = random.choice((BALL_SPEED_Y, -BALL_SPEED_Y))

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Check for collisions with walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y

# Main game loop
def main():
    clock = pygame.time.Clock()
    paddle1 = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddle2.move_up()
                elif event.key == pygame.K_DOWN:
                    paddle2.move_down()
                elif event.key == pygame.K_w:
                    paddle1.move_up()
                elif event.key == pygame.K_s:
                    paddle1.move_down()

        # Update
        ball.update()

        # Check for collisions with paddles
        if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
            ball.speed_x = -ball.speed_x

        # Check for out-of-bounds
        if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Draw
        screen.fill(BLACK)
        paddle1.draw()
        paddle2.draw()
        ball.draw()
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()
