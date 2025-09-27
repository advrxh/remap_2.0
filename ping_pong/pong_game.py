import pygame
import screeninfo
import numpy as np

# --- Screen Setup ---
monitor = screeninfo.get_monitors()[0]
SCREEN_WIDTH, SCREEN_HEIGHT = monitor.width, monitor.height
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Retro Hacker Pong")

# Hide mouse cursor
pygame.mouse.set_visible(False)

# --- Colors (Retro Hacker Theme) ---
BLACK = (0, 0, 0)
GREEN = (0, 255, 70)
DARK_GREEN = (0, 150, 50)
RED = (255, 50, 50)

# --- Fonts ---
font = pygame.font.SysFont("Consolas", 28, bold=True)
big_font = pygame.font.SysFont("Consolas", 72, bold=True)

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

# --- Background Music ---
# Replace "bg_music.mp3" with your own file
try:
    pygame.mixer.init()
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.play(-1)  # loop forever
except Exception as e:
    print("Background music not loaded:", e)


def generate_beep(frequency=440, duration_ms=200, volume=0.5):
    """Generate a simple beep sound using numpy for pygame (stereo)."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, False)

    # Generate sine wave
    wave = np.sin(frequency * 2 * np.pi * t) * volume

    # Convert to 16-bit integers
    wave = np.int16(wave * 32767)

    # Make it stereo by duplicating channels
    stereo_wave = np.column_stack((wave, wave))

    # Convert to Sound
    sound = pygame.sndarray.make_sound(stereo_wave)
    return sound


beep_paddle = generate_beep(800, 100, 0.6)   # higher beep
beep_life = generate_beep(200, 300, 0.6)     # lower beep

print("Retro Hacker Pong started. Q=Quit, SPACE=Pause/Resume")

def draw_background():
    """Retro-style scanline background."""
    screen.fill(BLACK)
    for y in range(0, SCREEN_HEIGHT, 4):
        pygame.draw.line(screen, DARK_GREEN, (0, y), (SCREEN_WIDTH, y))

while running:
    draw_background()

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused  # toggle pause

    if not paused and lives > 0:
        # --- Mouse Control for Paddle ---
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
            beep_paddle.play()

        # Missed the ball
        if ball_y > SCREEN_HEIGHT:
            lives -= 1
            beep_life.play()
            ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            ball_dx, ball_dy = 6, -6

    # --- Draw Paddle & Ball ---
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=5)
    pygame.draw.ellipse(screen, RED, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # --- Draw Score & Lives ---
    score_text = font.render(f"SCORE: {score}", True, GREEN)
    lives_text = font.render(f"LIVES: {lives}", True, GREEN)
    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))

    # --- Instructions ---
    instr_text = font.render("[Q] Quit | [SPACE] Pause/Resume", True, GREEN)
    screen.blit(instr_text, (SCREEN_WIDTH//2 - instr_text.get_width()//2, 20))

    # --- Game Over ---
    if lives <= 0:
        game_over_text = big_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        quit_text = font.render("Press Q to Quit", True, GREEN)
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 50))

    # --- Pause Screen ---
    if paused and lives > 0:
        pause_text = big_font.render("PAUSED", True, GREEN)
        screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

