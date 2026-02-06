"""
Ping-Pong Game - A classic two-player paddle game built with Pygame.
Controls: Player 1 (Left) - W/S, Player 2 (Right) - Up/Down arrows
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
PADDLE_SPEED = 8
BALL_SPEED = 7
WINNING_SCORE = 10
FPS = 60

# Colors (ping pong table style)
TABLE_GREEN = (27, 94, 32)       # Classic table felt green
PADDLE_COLOR = (220, 20, 60)      # Red paddles
BALL_COLOR = (255, 255, 255)      # White ball
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (255, 100, 150)
WHITE_LINE = (255, 255, 255)      # Table boundary & net

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong")
clock = pygame.time.Clock()


class Paddle:
    """Player paddle that moves up and down."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self, direction):
        """Move paddle. direction: -1 up, 1 down."""
        self.rect.y += direction * self.speed
        self.rect.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def draw(self):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect, border_radius=4)


class Ball:
    """Ball with velocity and bounce logic."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        angle = random.uniform(-0.6, 0.6)
        direction = random.choice([-1, 1])
        self.vx = direction * BALL_SPEED * (0.7 + 0.3 * abs(angle))
        self.vy = BALL_SPEED * angle

    def move(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # Bounce off top and bottom
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = abs(self.vy)
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vy = -abs(self.vy)

    def draw(self):
        pygame.draw.ellipse(screen, BALL_COLOR, self.rect)


def draw_table():
    """Draw ping pong table: green surface with white boundary lines and net."""
    # Table surface (green)
    screen.fill(TABLE_GREEN)
    # Top and bottom white boundary lines (table edges)
    line_thick = 4
    pygame.draw.rect(screen, WHITE_LINE, (0, 0, WIDTH, line_thick))
    pygame.draw.rect(screen, WHITE_LINE, (0, HEIGHT - line_thick, WIDTH, line_thick))
    # Left and right table edges (thin vertical lines in play area)
    pygame.draw.rect(screen, WHITE_LINE, (0, 0, line_thick, HEIGHT))
    pygame.draw.rect(screen, WHITE_LINE, (WIDTH - line_thick, 0, line_thick, HEIGHT))
    # Dashed center net
    dash_length = 20
    gap = 15
    x = WIDTH // 2 - 2
    y = 0
    while y < HEIGHT:
        pygame.draw.rect(screen, WHITE_LINE, (x, y, 4, dash_length))
        y += dash_length + gap


def draw_scores(score_left, score_right):
    """Draw score display."""
    font = pygame.font.Font(None, 72)
    left_text = font.render(str(score_left), True, TEXT_COLOR)
    right_text = font.render(str(score_right), True, TEXT_COLOR)
    screen.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 30))
    screen.blit(right_text, (3 * WIDTH // 4 - right_text.get_width() // 2, 30))


def draw_controls():
    """Draw control hints at bottom."""
    font = pygame.font.Font(None, 24)
    text = font.render("Player 1: W / S    |    Player 2: Up / Down    |    ESC: Quit", True, (200, 200, 200))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 35))


def show_winner(winner_text):
    """Show game over screen with winner."""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(TABLE_GREEN)
    screen.blit(overlay, (0, 0))

    font_large = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 36)
    title = font_large.render(winner_text, True, ACCENT_COLOR)
    subtitle = font_small.render("Press SPACE to play again  |  ESC to quit", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    waiting = False
                    break
        clock.tick(FPS)


def main():
    paddle_left = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle_right = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()
    score_left = 0
    score_right = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                paddle_left.move(-1)
            if keys[pygame.K_s]:
                paddle_left.move(1)
            if keys[pygame.K_UP]:
                paddle_right.move(-1)
            if keys[pygame.K_DOWN]:
                paddle_right.move(1)

            # Ball movement
            ball.move()

            # Collision with paddles
            if ball.rect.colliderect(paddle_left.rect):
                ball.rect.left = paddle_left.rect.right
                ball.vx = abs(ball.vx) * 1.05
                # Slight angle based on where ball hit paddle
                hit_pos = (ball.rect.centery - paddle_left.rect.centery) / (PADDLE_HEIGHT / 2)
                ball.vy += hit_pos * 2
            if ball.rect.colliderect(paddle_right.rect):
                ball.rect.right = paddle_right.rect.left
                ball.vx = -abs(ball.vx) * 1.05
                hit_pos = (ball.rect.centery - paddle_right.rect.centery) / (PADDLE_HEIGHT / 2)
                ball.vy += hit_pos * 2

            # Score when ball goes past paddle
            if ball.rect.left <= 0:
                score_right += 1
                ball.reset()
                if score_right >= WINNING_SCORE:
                    game_over = True
            if ball.rect.right >= WIDTH:
                score_left += 1
                ball.reset()
                if score_left >= WINNING_SCORE:
                    game_over = True

        # Draw everything
        draw_table()
        draw_scores(score_left, score_right)
        draw_controls()
        paddle_left.draw()
        paddle_right.draw()
        ball.draw()

        if game_over:
            winner = "Player 1 Wins!" if score_left >= WINNING_SCORE else "Player 2 Wins!"
            show_winner(winner)
            # Reset game
            score_left = 0
            score_right = 0
            paddle_left.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
            paddle_right.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
            ball.reset()
            game_over = False

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
