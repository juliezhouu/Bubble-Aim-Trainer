import math
import random
import time
import pygame

# initialize pygame 
pygame.init()

# window setup 
SCREEN_W, SCREEN_H = 800, 600
DISPLAY = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption(" Aim Trainer")

# game settings
SPAWN_DELAY =300  # milliseconds
SPAWN_EVENT = pygame.USEREVENT
MARGIN = 35
UI_BAR = 55
PLAYER_HEARTS = 4

# colour palette 
BLUSH_BG = (255, 235, 245)
SOFT_PINK = (255, 190, 210)
CANDY_PINK = (255, 135, 170)
CREAM = (255, 248, 250)
CHARCOAL = (40, 40, 40)

# font
MAIN_FONT = pygame.font.SysFont("segoe ui", 26, bold=False)

# --- background img for endscreen
END_BG = pygame.image.load(r"C:\Users\julie\Downloads\end_bg.png")  
END_BG = pygame.transform.scale(END_BG, (SCREEN_W, SCREEN_H))



# target class
class Bubble:

    MAX_RADIUS = 33
    GROW_SPEED = 0.23
    SHADE_MAIN = CANDY_PINK
    SHADE_ALT = CREAM

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.expanding = True

    def update(self):
        """Expand outward, then shrink when full."""
        if self.radius + self.GROW_SPEED >= self.MAX_RADIUS:
            self.expanding = False
        if self.expanding:
            self.radius += self.GROW_SPEED
        else:
            self.radius -= self.GROW_SPEED

    def draw(self, surface):
        """Draw layered rings for the bubble effect."""
        pygame.draw.circle(surface, self.SHADE_MAIN, (self.x, self.y), int(self.radius))
        pygame.draw.circle(surface, self.SHADE_ALT, (self.x, self.y), int(self.radius * 0.8))
        pygame.draw.circle(surface, self.SHADE_MAIN, (self.x, self.y), int(self.radius * 0.6))
        pygame.draw.circle(surface, self.SHADE_ALT, (self.x, self.y), int(self.radius * 0.4))

    def is_clicked(self, mx, my):
        """Detect hit using distance formula"""
        dist = math.sqrt((mx - self.x) ** 2 + (my - self.y) ** 2)
        return dist <= self.radius



# drawing functions

def render_scene(surface, bubbles):
    surface.fill(BLUSH_BG)
    for b in bubbles:
        b.draw(surface)


def nice_time(seconds):
    milli = math.floor(int(seconds * 1000 % 1000) / 100)
    sec = int(round(seconds % 60, 1))
    mins = int(seconds // 60)
    return f"{mins:02d}:{sec:02d}.{milli}"


def render_ui(surface, elapsed, hits, fails):
    pygame.draw.rect(surface, SOFT_PINK, (0, 0, SCREEN_W, UI_BAR))

    time_txt = MAIN_FONT.render(f"Time: {nice_time(elapsed)}", True, CHARCOAL)
    speed = round(hits / elapsed, 1) if elapsed > 0 else 0
    speed_txt = MAIN_FONT.render(f"Speed: {speed} t/s", True, CHARCOAL)
    hit_txt = MAIN_FONT.render(f"Hits: {hits}", True, CHARCOAL)
    life_txt = MAIN_FONT.render(f"Lives: {PLAYER_HEARTS - fails}", True, CHARCOAL)

    surface.blit(time_txt, (15, 10))
    surface.blit(speed_txt, (210, 10))
    surface.blit(hit_txt, (440, 10))
    surface.blit(life_txt, (660, 10))


# end screen 
def final_screen(surface, elapsed, hits, clicks):
    # draw background image
    surface.blit(END_BG, (0, 0))
    overlay = pygame.Surface((SCREEN_W, SCREEN_H))
    overlay.set_alpha(70)
    overlay.fill((255, 200, 220))
    surface.blit(overlay, (0, 0))

    # stats
    accuracy = round(hits / clicks * 100, 1) if clicks > 0 else 0
    speed = round(hits / elapsed, 1) if elapsed > 0 else 0

    def center_text(txt, y, color=CHARCOAL, size=28, bold=False):
        font = pygame.font.SysFont("segoe ui", size, bold=bold)
        label = font.render(txt, True, color)
        surface.blit(label, (SCREEN_W / 2 - label.get_width() / 2, y))

    # render centered labels
    center_text("Game Over lol", 90, CHARCOAL, 42, True)
    center_text(f"Time Played: {nice_time(elapsed)}", 180)
    center_text(f"Total Hits: {hits}", 240)
    center_text(f"Accuracy: {accuracy}%", 300)
    center_text(f"Speed: {speed} bubbles/sec", 360)
    center_text("Press any key to exit", 470, CHARCOAL, 24)
    pygame.display.update()

    # wait for player to exit
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN:
                waiting = False
                pygame.quit()
                quit()


# main game loop purr
def main():
    running = True
    bubbles = []
    clock = pygame.time.Clock()

    hit_count = 0
    total_clicks = 0
    missed = 0
    start = time.time()

    pygame.time.set_timer(SPAWN_EVENT, SPAWN_DELAY)

    while running:
        clock.tick(60)
        clicked = False
        mouse = pygame.mouse.get_pos()
        elapsed = time.time() - start

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
            if e.type == SPAWN_EVENT:
                x = random.randint(MARGIN, SCREEN_W - MARGIN)
                y = random.randint(MARGIN + UI_BAR, SCREEN_H - MARGIN)
                bubbles.append(Bubble(x, y))
            if e.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                total_clicks += 1

        for b in bubbles[:]:
            b.update()
            if b.radius <= 0:
                bubbles.remove(b)
                missed += 1
            elif clicked and b.is_clicked(*mouse):
                bubbles.remove(b)
                hit_count += 1

        if missed >= PLAYER_HEARTS:
            final_screen(DISPLAY, elapsed, hit_count, total_clicks)

        render_scene(DISPLAY, bubbles)
        render_ui(DISPLAY, elapsed, hit_count, missed)
        pygame.display.update()

    pygame.quit()


# -------------------- #
# run the game
# -------------------- #
if __name__ == "__main__":

    main()
