import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
BIRD_WIDTH, BIRD_HEIGHT = 50, 50
PIPE_WIDTH, PIPE_HEIGHT = 50, random.randint(150, 400)
PIPE_GAP = 200
GRAVITY = 0.25
FLAP_SPEED = -5
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the screen   
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_img = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
pipe_img.fill((0, 255, 0))

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel_y = 0

    def flap(self):
        self.vel_y = FLAP_SPEED

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(150, 400)
        self.width = PIPE_WIDTH
        self.height = PIPE_HEIGHT

    def update(self):
        self.x -= 2

    def draw(self):
        screen.blit(pipe_img, (self.x, 0))
        screen.blit(pipe_img, (self.x, self.y + PIPE_GAP))

# Check collisions
def collide(bird, pipes):
    if bird.y <= 0 or bird.y + BIRD_HEIGHT >= HEIGHT:
        return True

    for pipe in pipes:
        if (bird.x + BIRD_WIDTH >= pipe.x and bird.x <= pipe.x + PIPE_WIDTH) and \
            (bird.y <= pipe.y or bird.y + BIRD_HEIGHT >= pipe.y + PIPE_GAP):
            return True

    return False

# Main game loop
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Update
        bird.update()
        for pipe in pipes:
            pipe.update()

        # Generate new pipes
        if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        # Check collisions
        if collide(bird, pipes):
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        # Draw
        screen.fill(BLACK)
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
