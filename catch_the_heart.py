import random
import sys

import pygame


# Screen settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
PINK_TOP = (255, 182, 193)
PURPLE_BOTTOM = (186, 85, 211)
PLAYER_COLOR = (255, 105, 180)
HEART_COLOR = (255, 20, 147)
TEXT_COLOR = (255, 255, 255)

# Game rules
TARGET_SCORE = 15
HEART_FALL_SPEED = 4
PLAYER_SPEED = 7


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Heart")
clock = pygame.time.Clock()

score_font = pygame.font.SysFont("arial", 36, bold=True)
message_font = pygame.font.SysFont("arial", 42, bold=True)
sub_message_font = pygame.font.SysFont("arial", 28)


def draw_vertical_gradient(surface, top_color, bottom_color):
    """Draw a smooth top-to-bottom gradient background."""
    for y in range(HEIGHT):
        blend = y / HEIGHT
        r = int(top_color[0] * (1 - blend) + bottom_color[0] * blend)
        g = int(top_color[1] * (1 - blend) + bottom_color[1] * blend)
        b = int(top_color[2] * (1 - blend) + bottom_color[2] * blend)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


def heart_points(center_x, center_y, size):
    """Return polygon points that resemble a simple heart shape."""
    return [
        (center_x, center_y + size // 2),
        (center_x - size, center_y - size // 6),
        (center_x - size // 2, center_y - size),
        (center_x, center_y - size // 2),
        (center_x + size // 2, center_y - size),
        (center_x + size, center_y - size // 6),
    ]


def draw_heart(surface, x, y, size=20, color=HEART_COLOR):
    """Draw a heart using two circles and a polygon."""
    radius = size // 2
    pygame.draw.circle(surface, color, (x - radius, y - radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y - radius), radius)
    pygame.draw.polygon(surface, color, heart_points(x, y, size))


def draw_wrapped_text(surface, text, font, color, rect, line_spacing=6):
    """Render wrapped multi-line text inside a given rectangle."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        trial = f"{current_line} {word}".strip()
        if font.size(trial)[0] <= rect.width:
            current_line = trial
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    total_height = sum(font.size(line)[1] for line in lines) + line_spacing * (len(lines) - 1)
    y = rect.y + (rect.height - total_height) // 2

    for line in lines:
        line_surface = font.render(line, True, color)
        line_x = rect.centerx - line_surface.get_width() // 2
        surface.blit(line_surface, (line_x, y))
        y += line_surface.get_height() + line_spacing


player = pygame.Rect(WIDTH // 2 - 45, HEIGHT - 70, 90, 30)
heart_size = 22
heart_x = random.randint(heart_size, WIDTH - heart_size)
heart_y = -heart_size
score = 0
unlocked = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not unlocked:
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        player.x = max(0, min(WIDTH - player.width, player.x))

        heart_y += HEART_FALL_SPEED
        if heart_y > HEIGHT + heart_size:
            heart_x = random.randint(heart_size, WIDTH - heart_size)
            heart_y = -heart_size

        heart_rect = pygame.Rect(
            heart_x - heart_size,
            heart_y - heart_size,
            heart_size * 2,
            heart_size * 2,
        )

        if player.colliderect(heart_rect):
            score += 1
            heart_x = random.randint(heart_size, WIDTH - heart_size)
            heart_y = -heart_size

            if score >= TARGET_SCORE:
                unlocked = True

    draw_vertical_gradient(screen, PINK_TOP, PURPLE_BOTTOM)

    # Player character
    pygame.draw.rect(screen, PLAYER_COLOR, player, border_radius=12)

    # Falling heart
    if not unlocked:
        draw_heart(screen, heart_x, heart_y, size=heart_size * 2 // 1)

    # Score display
    score_surface = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_surface, (20, 20))

    if unlocked:
        title = "✨ New Option Unlocked ✨"
        message = (
            "You unlocked my heart ❤️. I love you soo much babydoll and always be there "
            "for you. You are the best thing that ever happened to me and the best "
            "girlfriend. Love you forever 💞"
        )

        title_surface = message_font.render(title, True, WHITE)
        title_x = WIDTH // 2 - title_surface.get_width() // 2
        title_y = HEIGHT // 2 - 130
        screen.blit(title_surface, (title_x, title_y))

        text_rect = pygame.Rect(90, HEIGHT // 2 - 40, WIDTH - 180, 180)
        draw_wrapped_text(screen, message, sub_message_font, WHITE, text_rect)

    pygame.display.flip()
    clock.tick(FPS)
