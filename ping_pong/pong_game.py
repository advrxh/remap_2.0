import pygame
import screeninfo

# --- Screen Setup ---
monitor = screeninfo.get_monitors()[0]
SCREEN_WIDTH, SCREEN_HEIGHT = monitor.width, monitor.height
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Ping Pong (Mouse Control)")

# Hide mouse cursor
pygame.mouse.set_visible(False)

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Fonts ---
font = pygame.font.SysFont("Arial", 36, bold=True)

# --- Paddle ---
PADDLE_WIDTH, PADDLE_HEIGHT = 150, 20
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = SCREEN_HEIGHT - 50

# --- Ball ---
BALL_SIZE = 20
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx, ball_dy = 6, -6

# --- Game State ---
score = 0
lives = 3
paused = False
running = True
clock = pygame.time.Clock()

print("Pong game started (mouse controls). Press Q to quit.")

while running:
    screen.fill(BLACK)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Quit
                running = False
            elif event.key == pygame.K_p:  # Pause
                paused = True
            elif event.key == pygame.K_r:  # Resume
                paused = False

    if not paused and lives > 0:
        # --- Mouse Control ---
        mouse_x, _ = pygame.mouse.get_pos()
        paddle_x = mouse_x - PADDLE_WIDTH // 2
        paddle_x = max(0, min(SCREEN_WIDTH - PADDLE_WIDTH, paddle_x))

        # --- Move Ball ---
        ball_x += ball_dx
        ball_y += ball_dy

        # Bounce on walls
        if ball_x <= 0 or ball_x >= SCREEN_WIDTH - BALL_SIZE:
            ball_dx *= -1
        if ball_y <= 0:
            ball_dy *= -1

        # Bounce on paddle
        if (paddle_y <= ball_y + BALL_SIZE <= paddle_y + PADDLE_HEIGHT) and (
            paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH
        ):
            ball_dy *= -1
            score += 1

        # Missed the ball
        if ball_y > SCREEN_HEIGHT:
            lives -= 1
            ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            ball_dx, ball_dy = 6, -6

    # --- Draw Paddle & Ball ---
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # --- Draw Score & Lives ---
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))

    # --- Instructions ---
    instr_text = font.render("Press Q to Quit | P to Pause | R to Resume", True, WHITE)
    screen.blit(instr_text, (SCREEN_WIDTH//2 - instr_text.get_width()//2, 20))

    # --- Game Over ---
    if lives <= 0:
        game_over_text = font.render("GAME OVER! Press Q to quit.", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2))

    # --- Pause Screen ---
    if paused and lives > 0:
        pause_text = font.render("PAUSED - Press R to resume", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

