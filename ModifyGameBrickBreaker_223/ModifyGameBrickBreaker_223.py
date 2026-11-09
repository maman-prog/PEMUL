import pygame
import random
import sys
import math

pygame.init()

# Dimensions of the screen
WIDTH, HEIGHT = 800, 600

# Palette Warna Synthwave / Cyberpunk Neon
BG_COLOR = (12, 14, 24)
PANEL_COLOR = (20, 24, 42)
WHITE = (255, 255, 255)
NEON_PINK = (255, 45, 118)
NEON_CYAN = (0, 240, 255)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (255, 214, 0)
NEON_PURPLE = (176, 38, 255)
GRAY = (100, 110, 140)

font_title = pygame.font.Font(None, 64)
font_large = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 18)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker - Ultimate Masterpiece Edition")

clock = pygame.time.Clock()
FPS = 60


# Floating Text untuk Skor
class FloatingText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.alpha = 255
        self.vy = -1.5

    def update(self):
        self.y += self.vy
        self.alpha = max(0, self.alpha - 6)

    def display(self, surface):
        if self.alpha > 0:
            text_surf = font_medium.render(self.text, True, self.color)
            text_surf.set_alpha(self.alpha)
            surface.blit(text_surf, (self.x, self.y))


# Power-Up Item yang Jatuh
class PowerUp:
    def __init__(self, x, y, p_type):
        self.x = x
        self.y = y
        self.type = p_type  # 'expand', 'multiball', 'life'
        self.width = 30
        self.height = 15
        self.speed = 3
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        if self.type == 'expand':
            self.color = NEON_GREEN
            self.label = "EXT"
        elif self.type == 'multiball':
            self.color = NEON_YELLOW
            self.label = "MULTI"
        else:
            self.color = NEON_PINK
            self.label = "+1UP"

    def update(self):
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, WHITE, self.rect, 1, border_radius=4)
        txt = font_small.render(self.label, True, BLACK if self.type=='multilball' else WHITE)
        surface.blit(txt, (self.x + 4, self.y + 2))


# Particle Efek Ledakan
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 6)
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(20, 40)
        self.max_life = self.life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95
        self.vy *= 0.95
        self.life -= 1

    def display(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


# Striker (Paddle)
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self, surface):
        glow_rect = pygame.Rect(self.posx - 2, self.posy - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(surface, (0, 150, 200), glow_rect, border_radius=10)
        pygame.draw.rect(surface, self.color, self.strikerRect, border_radius=8)
        pygame.draw.line(surface, WHITE, (self.posx + 10, self.posy + 3), (self.posx + self.width - 10, self.posy + 3), 2)

    def update(self, xFac, mouse_x=None):
        if mouse_x is not None:
            self.posx = mouse_x - self.width // 2
        elif xFac != 0:
            self.posx += self.speed * xFac

        if self.posx <= 15:
            self.posx = 15
        elif self.posx + self.width >= WIDTH - 15:
            self.posx = WIDTH - 15 - self.width

        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def getRect(self):
        return self.strikerRect


# Block
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width = width
        self.height = height
        self.color = color
        
        if color == NEON_PURPLE:
            self.health = 200
        elif color == NEON_YELLOW:
            self.health = 150
        else:
            self.health = 100

        self.blockRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self, surface):
        if self.health > 0:
            current_color = self.color
            if self.health == 100 and self.color == NEON_PURPLE:
                current_color = GRAY
                
            pygame.draw.rect(surface, current_color, self.blockRect, border_radius=5)
            pygame.draw.rect(surface, WHITE, self.blockRect, 1, border_radius=5)

    def hit(self):
        self.health -= 100

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health


# Ball dengan Trail
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = random.choice([-1, 1]), -1
        self.trail = []

    def display(self, surface):
        for i, pos in enumerate(self.trail):
            alpha_radius = max(1, int(self.radius * (i / len(self.trail))))
            pygame.draw.circle(surface, NEON_CYAN, (int(pos[0]), int(pos[1])), alpha_radius)

        pygame.draw.circle(surface, self.color, (int(self.posx), int(self.posy)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.posx), int(self.posy)), self.radius - 3)

    def update(self):
        self.trail.append((self.posx, self.posy))
        if len(self.trail) > 8:
            self.trail.pop(0)

        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        if self.posx - self.radius <= 15:
            self.posx = 15 + self.radius
            self.xFac *= -1
        elif self.posx + self.radius >= WIDTH - 15:
            self.posx = WIDTH - 15 - self.radius
            self.xFac *= -1

        if self.posy - self.radius <= 70:
            self.posy = 70 + self.radius
            self.yFac *= -1

        if self.posy >= HEIGHT:
            return True

        return False

    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)


def populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap):
    listOfBlocks = []
    start_y = 90
    start_x = 45
    for i in range(start_x, WIDTH - blockWidth - 30, blockWidth + horizontalGap):
        for j in range(start_y, start_y + 180, blockHeight + verticalGap):
            color = random.choice([NEON_PINK, NEON_CYAN, NEON_GREEN, NEON_YELLOW, NEON_PURPLE])
            listOfBlocks.append(Block(i, j, blockWidth, blockHeight, color))
    return listOfBlocks


def showMenuScreen():
    screen.fill(BG_COLOR)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (20, 25, 45), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (20, 25, 45), (0, y), (WIDTH, y), 1)

    title_text = font_title.render("BLOCK BREAKER", True, NEON_CYAN)
    sub_text = font_medium.render("MASTERPIECE EDITION + POWER-UPS", True, NEON_PINK)
    prompt_text = font_large.render("PRESS [ SPACE ] TO START", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 60))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


def showGameOverScreen(score):
    screen.fill(BG_COLOR)
    msg1 = font_title.render("GAME OVER", True, NEON_PINK)
    msg2 = font_large.render(f"Final Score: {score}", True, WHITE)
    msg3 = font_medium.render("Press 'R' to Restart or 'ESC' to Quit", True, NEON_YELLOW)

    screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 70))
    screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 - 10))
    screen.blit(msg3, (WIDTH // 2 - msg3.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False


def main():
    showMenuScreen()

    running = True
    lives = 3
    score = 0
    level = 1

    striker = Striker(WIDTH // 2 - 60, HEIGHT - 50, 120, 16, 9, NEON_CYAN)
    strikerXFac = 0

    balls = [Ball(WIDTH // 2, HEIGHT - 150, 8, 5.5, WHITE)]

    blockWidth, blockHeight = 65, 20
    horizontalGap, verticalGap = 12, 12

    listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)
    particles = []
    floating_texts = []
    powerups = []
    
    screen_shake = 0

    while running:
        # Render ke dalam surface buffer untuk efek screen shake
        render_surface = pygame.Surface((WIDTH, HEIGHT))
        render_surface.fill(BG_COLOR)

        # Latar Belakang Grid
        for x in range(0, WIDTH, 50):
            pygame.draw.line(render_surface, (18, 22, 40), (x, 0), (x, HEIGHT), 1)

        pygame.draw.rect(render_surface, (30, 35, 60), (0, 0, 15, HEIGHT))
        pygame.draw.rect(render_surface, (30, 35, 60), (WIDTH - 15, 0, 15, HEIGHT))

        # HUD Panel Atas
        pygame.draw.rect(render_surface, PANEL_COLOR, (0, 0, WIDTH, 65))
        pygame.draw.line(render_surface, NEON_CYAN, (0, 65), (WIDTH, 65), 2)

        scoreText = font_large.render(f"SCORE : {score}", True, WHITE)
        levelText = font_large.render(f"LEVEL : {level}", True, NEON_YELLOW)
        livesText = font_large.render(f"LIVES : {lives}", True, NEON_PINK)

        render_surface.blit(scoreText, (30, 20))
        render_surface.blit(levelText, (WIDTH // 2 - levelText.get_width() // 2, 20))
        render_surface.blit(livesText, (WIDTH - 140, 20))

        if not listOfBlocks:
            level += 1
            listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)
            balls = [Ball(WIDTH // 2, HEIGHT - 150, 8, 5.5 + (level * 0.5), WHITE)]
            powerups.clear()

        mouse_x = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0
            if event.type == pygame.MOUSEMOTION:
                mouse_x = event.pos[0]

        # --- Collision & Physics ---
        for ball in balls[:]:
            ball_rect = ball.getRect()

            # Striker Collision
            if ball_rect.colliderect(striker.getRect()):
                ball.yFac = -1
                offset = (ball.posx - (striker.posx + striker.width / 2)) / (striker.width / 2)
                ball.xFac = offset * 2.0

            # Block Collision
            for block in listOfBlocks[:]:
                if ball_rect.colliderect(block.getRect()):
                    block.hit()
                    
                    for _ in range(8):
                        particles.append(Particle(block.posx + block.width//2, block.posy + block.height//2, block.color))

                    if abs(ball.posx - block.getRect().left) < 6 or abs(ball.posx - block.getRect().right) < 6:
                        ball.xFac *= -1
                    else:
                        ball.yFac *= -1

                    if block.getHealth() <= 0:
                        earned_score = 25 * level
                        score += earned_score
                        floating_texts.append(FloatingText(block.posx + block.width//2, block.posy, f"+{earned_score}", NEON_GREEN))
                        
                        # Peluang 25% menjatuhkan Power-Up
                        if random.random() < 0.25:
                            p_type = random.choice(['expand', 'multiball', 'life'])
                            powerups.append(PowerUp(block.posx + block.width//2 - 15, block.posy, p_type))

                        listOfBlocks.remove(block)
                    break

            if ball.update():
                balls.remove(ball)

        # Jika semua bola jatuh
        if len(balls) == 0:
            lives -= 1
            screen_shake = 15  # Guncangan layar
            if lives <= 0:
                shouldRestart = showGameOverScreen(score)
                if shouldRestart:
                    main()
                    return
                else:
                    break
            else:
                balls.append(Ball(striker.posx + striker.width//2, striker.posy - 20, 8, 5.5, WHITE))
                pygame.time.wait(400)

        # Update & Tangkap Power-Ups
        for pu in powerups[:]:
            pu.update()
            pu.display(render_surface)
            if pu.rect.colliderect(striker.getRect()):
                if pu.type == 'expand':
                    striker.width = min(180, striker.width + 30)
                elif pu.type == 'multiball':
                    if len(balls) > 0:
                        b = balls[0]
                        balls.append(Ball(b.posx, b.posy, 8, b.speed, WHITE))
                elif pu.type == 'life':
                    lives += 1
                powerups.remove(pu)
            elif pu.y > HEIGHT:
                powerups.remove(pu)

        # Update Partikel & Floating Text
        for p in particles[:]:
            p.update()
            p.display(render_surface)
            if p.life <= 0:
                particles.remove(p)

        for ft in floating_texts[:]:
            ft.update()
            ft.display(render_surface)
            if ft.alpha <= 0:
                floating_texts.remove(ft)

        # Update Pemukul & Bola
        striker.update(strikerXFac, mouse_x)
        striker.display(render_surface)

        for ball in balls:
            ball.display(render_surface)

        for block in listOfBlocks:
            block.display(render_surface)

        # Terapkan Screen Shake jika aktif
        shake_x, shake_y = 0, 0
        if screen_shake > 0:
            shake_x = random.randint(-4, 4)
            shake_y = random.randint(-4, 4)
            screen_shake -= 1

        screen.fill(BG_COLOR)
        screen.blit(render_surface, (shake_x, shake_y))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()