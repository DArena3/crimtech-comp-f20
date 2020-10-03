import random
import pygame
import sys
import math
import time

# global variables
WIDTH = 24
HEIGHT = 24
SIZE = 20
SCREEN_WIDTH = WIDTH * SIZE
SCREEN_HEIGHT = HEIGHT * SIZE

DIR = {
    'u' : (0, -1), # north is -y
    'd' : (0, 1),
    'l' : (-1,0),
    'r' : (1,0)
}

# Implements feature 12
THEMES = {
    "classic" : {
        "gcolor1" : (169,215,81),
        "gcolor2" : (162,208,73),
        "hcolor" : (40,50,100),
        "tcolor" : (90,130,255),
        "acolor" : (233, 70, 29),
        "xcolor" : (0,0,0)
    },
    "spaceship" : {
        "gcolor1" : (0,0,0),
        "gcolor2" : (10,10,40),
        "hcolor" : (210,10,10),
        "tcolor" : (230,80,80),
        "acolor" : (0,175,0),
        "xcolor" : (233, 70, 29)
    },
    "party" : {
        "gcolor1" : (159,0,245),
        "gcolor2" : (144,4,219),
        "hcolor" : (219,7,194),
        "tcolor" : (242,73,222),
        "acolor" : (10,19,191),
        "xcolor" : (200,200,0)
    }
}

THEME = "classic"

class Snake(object):
    l = 1
    body = [(WIDTH // 2 + 1, HEIGHT // 2),(WIDTH // 2, HEIGHT // 2)]
    direction = 'r'
    dead = True
    hcolor = tuple()
    tcolor = tuple()

    def __init__(self):
        self.hcolor = THEMES[THEME]["hcolor"]
        self.tcolor = THEMES[THEME]["tcolor"]
        pass
    
    def get_color(self, i):
        hc = self.hcolor
        tc = self.tcolor
        return tuple(map(lambda x,y: (x * (self.l - i) + y * i ) / self.l, hc, tc))

    def get_head(self):
        return self.body[0]

    def turn(self, dir):
        self.direction = dir
        pass

    def collision(self, x, y):
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            # print("Died on edge")
            return True

        for i in range(1, len(self.body)):
            if x == self.body[i][0] and y == self.body[i][1]:
                # print("died because i hit ", (self.body[i][0], self.body[i][1]))
                return True

        return False

    """def coyote_time(self):
        start = time.perf_counter()
        start_dir = self.direction

        while (time.perf_counter() - start) < 0.001:
            print(time.perf_counter() - start)
            self.check_events()
            if self.direction != start_dir:
                return True

        return False"""

    def move(self):
        if self.collision(self.get_head()[0] + DIR[self.direction][0], self.get_head()[1] + DIR[self.direction][1]):
            # print("tried to collide with", (self.get_head()[0] + DIR[self.direction][0], self.get_head()[1] + DIR[self.direction][1]), "body:", self.body)
            self.kill()
            pass
        else:
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i] = self.body[i - 1]

            self.body[0] = (self.body[0][0] + DIR[self.direction][0], self.body[0][1] + DIR[self.direction][1])
            # print("moving head to ", (self.body[0][0] + DIR[self.direction][0], self.body[0][1] + DIR[self.direction][1]))
            pass

    # Implements feature 11
    def kill(self):
        self.l = 1
        self.body = [(WIDTH // 2 + 1, HEIGHT // 2),(WIDTH // 2, HEIGHT // 2)]
        self.direction = 'r'
        self.dead = True

    def draw(self, surface):
        for i in range(len(self.body)):
            p = self.body[i]
            pos = (p[0] * SIZE, p[1] * SIZE)
            r = pygame.Rect(pos, (SIZE, SIZE))
            pygame.draw.rect(surface, self.get_color(i), r)

    def handle_keypress(self, k):
        if k == pygame.K_UP:
            self.turn('u')
        if k == pygame.K_DOWN:
            self.turn('d')
        if k == pygame.K_LEFT:
            self.turn('l')
        if k == pygame.K_RIGHT:
            self.turn('r')
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue
            self.handle_keypress(event.key)
    
    # Implements feature 10
    def wait_for_key(self):
        key_pressed = False

        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type != pygame.KEYDOWN:
                    continue
                key_pressed = True
                self.handle_keypress(event.key)

        self.dead = False
        pass


# returns an integer between 0 and n, inclusive.
def rand_int(n):
    return random.randint(0, n)

class Apple(object):
    position = (10,10)
    color = tuple()

    def __init__(self):
        self.color = THEMES[THEME]["acolor"]
        self.place([])

    def place(self, snake):
        placed = False

        while (not placed and len(snake) > 0):
            self.position = (rand_int(WIDTH - 1), rand_int(HEIGHT - 1))
            # print("now placing the apple at", self.position)
            
            for i in range(len(snake)):
                if self.position[0] == snake[i][0] and self.position[1] == snake[i][1]:
                    placed = False
                    break
                else:
                    placed = True
        pass

    def draw(self, surface):
        pos = (self.position[0] * SIZE, self.position[1] * SIZE)
        r = pygame.Rect(pos, (SIZE, SIZE))
        pygame.draw.rect(surface, self.color, r)

def draw_grid(surface):
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            r = pygame.Rect((x * SIZE, y * SIZE), (SIZE, SIZE))
            color = THEMES[THEME]["gcolor1"] if (x+y) % 2 == 0 else THEMES[THEME]["gcolor2"]
            pygame.draw.rect(surface, color, r)

# Implements feature 9
def tick_timer(n):
    return 20 * (1 / (1 + math.exp(-0.06 * n)))

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    global THEME 
    if len(sys.argv) > 1:
        if sys.argv[1] == "spaceship":
            THEME = "spaceship"
        elif sys.argv[1] == "party":
            THEME = "party"

    font = pygame.font.SysFont("arial", 16)
    text_color = THEMES[THEME]["xcolor"]
    text = "Score: 0"

    display_text = font.render(text, True, text_color)
    text_rect = display_text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SIZE) 

    draw_grid(surface)
    pygame.display.set_caption("David Arena: Snek")

    snake = Snake()
    apple = Apple()

    score = 0

    draw_grid(surface) 
    snake.draw(surface)
    apple.draw(surface)
    screen.blit(surface, (0,0))
    screen.blit(display_text, text_rect)
    pygame.display.update()
    
    while True:
        if snake.dead:
            # Implements feature 10
            snake.wait_for_key()
            score = 0
            text = "Score: " + str(score)
            display_text = font.render(text, True, text_color)
            screen.blit(display_text, text_rect)
        # Implements feature 9
        clock.tick(tick_timer(snake.l))

        snake.check_events()
        draw_grid(surface) 
        snake.move()

        snake.draw(surface)
        apple.draw(surface)

        if (snake.get_head()[0] == apple.position[0] and snake.get_head()[1] == apple.position[1]):
            snake.body.insert(0, (apple.position[0], apple.position[1]))
            apple.place(snake.body)
            snake.l += 1
            score += 1
            # print("speed=", tick_timer(snake.l))
            text = "Score: " + str(score)
            display_text = font.render(text, True, text_color)
            # print(time.perf_counter())

        screen.blit(surface, (0,0))
        screen.blit(display_text, text_rect)

        pygame.display.update()
        if snake.dead:
            print('You died. Score: %d' % score)
            # pygame.quit()
            # sys.exit(0)

if __name__ == "__main__":
    main()