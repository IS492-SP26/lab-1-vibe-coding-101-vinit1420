import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 10
PADDLE_SPEED = 7

# Paddle properties
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball properties
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 5
ball_speed_y = 5

# Scoring
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

MAX_SCORE = 5
game_active = True

def reset_game():
    global player_score, opponent_score, ball, player_paddle, opponent_paddle, ball_speed_x, ball_speed_y, game_active
    player_score = 0
    opponent_score = 0
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = 5 * (1 if pygame.time.get_ticks() % 2 == 0 else -1) # Randomize initial ball direction
    ball_speed_y = 5 * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
    player_paddle.center = (50 + PADDLE_WIDTH // 2, HEIGHT // 2)
    opponent_paddle.center = (WIDTH - 50 - PADDLE_WIDTH // 2, HEIGHT // 2)
    game_active = True

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_active and event.key == pygame.K_SPACE:
                reset_game()

    if game_active:
        # Player paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_paddle.top > 0:
            player_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
            player_paddle.y += PADDLE_SPEED

        # Opponent AI (simple)
        if opponent_paddle.centery < ball.centery and opponent_paddle.bottom < HEIGHT:
            opponent_paddle.y += PADDLE_SPEED
        if opponent_paddle.centery > ball.centery and opponent_paddle.top > 0:
            opponent_paddle.y -= PADDLE_SPEED

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        
        # Ball collision with paddles
        if ball.colliderect(player_paddle):
            if abs(ball.left - player_paddle.right) < 10: # collision from right of player_paddle
                ball_speed_x *= -1
            elif abs(ball.bottom - player_paddle.top) < 10 and ball_speed_y > 0: # collision from top of player_paddle
                ball_speed_y *= -1
            elif abs(ball.top - player_paddle.bottom) < 10 and ball_speed_y < 0: # collision from bottom of player_paddle
                ball_speed_y *= -1

        if ball.colliderect(opponent_paddle):
            if abs(ball.right - opponent_paddle.left) < 10: # collision from left of opponent_paddle
                ball_speed_x *= -1
            elif abs(ball.bottom - opponent_paddle.top) < 10 and ball_speed_y > 0: # collision from top of opponent_paddle
                ball_speed_y *= -1
            elif abs(ball.top - opponent_paddle.bottom) < 10 and ball_speed_y < 0: # collision from bottom of opponent_paddle
                ball_speed_y *= -1

        # Scoring
        if ball.left <= 0:
            opponent_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1  # Reset ball direction
        if ball.right >= WIDTH:
            player_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1  # Reset ball direction

        # Check for game over
        if player_score >= MAX_SCORE or opponent_score >= MAX_SCORE:
            game_active = False

    # Drawing
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, WHITE, player_paddle)
    pygame.draw.rect(SCREEN, WHITE, opponent_paddle)
    pygame.draw.ellipse(SCREEN, WHITE, ball)
    pygame.draw.aaline(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Display scores
    player_text = font.render(str(player_score), True, WHITE)
    opponent_text = font.render(str(opponent_score), True, WHITE)
    SCREEN.blit(player_text, (WIDTH // 4, 20))
    SCREEN.blit(opponent_text, (WIDTH * 3 // 4 - opponent_text.get_width(), 20))

    if not game_active:
        game_over_text = font.render("Game Over!", True, WHITE)
        if player_score >= MAX_SCORE:
            winner_text = font.render("Player Wins!", True, WHITE)
        else:
            winner_text = font.render("Opponent Wins!", True, WHITE)
        restart_text = small_font.render("Press SPACE to Restart", True, WHITE)

        SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        SCREEN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 + 10))
        SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.flip()
    clock.tick(60) # Limit frame rate to 60 FPS