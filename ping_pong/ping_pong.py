import pygame

class PongGame:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("ESP Ping-Pong")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Paddle
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 20, 100
        self.paddle_y = self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2

        # Ball
        self.ball_radius = 15
        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        self.ball_speed_x = 5
        self.ball_speed_y = 4

    def update(self, gyro_data=None, sens_y=0.02):
        # Handle paddle movement from ESP
        if gyro_data and "gz" in gyro_data:
            delta = -gyro_data["gz"] * sens_y
            self.paddle_y += delta

        # Keep paddle in screen
        if self.paddle_y < 0:
            self.paddle_y = 0
        elif self.paddle_y + self.PADDLE_HEIGHT > self.HEIGHT:
            self.paddle_y = self.HEIGHT - self.PADDLE_HEIGHT

        # Move ball
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # Bounce off top/bottom
        if self.ball_y - self.ball_radius < 0 or self.ball_y + self.ball_radius > self.HEIGHT:
            self.ball_speed_y *= -1

        # Bounce off paddles
        if self.ball_x - self.ball_radius < self.PADDLE_WIDTH:
            if self.paddle_y < self.ball_y < self.paddle_y + self.PADDLE_HEIGHT:
                self.ball_speed_x *= -1
            else:
                # Missed, reset ball
                self.ball_x, self.ball_y = self.WIDTH // 2, self.HEIGHT // 2
        elif self.ball_x + self.ball_radius > self.WIDTH - self.PADDLE_WIDTH:
            # Right paddle AI (static)
            if self.HEIGHT//2 - self.PADDLE_HEIGHT//2 < self.ball_y < self.HEIGHT//2 + self.PADDLE_HEIGHT//2:
                self.ball_speed_x *= -1
            else:
                self.ball_x, self.ball_y = self.WIDTH // 2, self.HEIGHT // 2

    def draw(self):
        self.screen.fill((0,0,0))
        # Left paddle (ESP)
        pygame.draw.rect(self.screen, (0,255,0), (0, self.paddle_y, self.PADDLE_WIDTH, self.PADDLE_HEIGHT))
        # Right paddle (AI)
        pygame.draw.rect(self.screen, (255,0,0), (self.WIDTH - self.PADDLE_WIDTH, self.HEIGHT//2 - self.PADDLE_HEIGHT//2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT))
        # Ball
        pygame.draw.circle(self.screen, (255,255,255), (int(self.ball_x), int(self.ball_y)), self.ball_radius)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

