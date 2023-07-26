import curses
import time
from collections import deque
import sys

class Game:
    def __init__(self, width: int, height: int):
        self.score = 0
        self.high_score = 0
        self.speed = 1
        self.width = width
        self.height = height
        self.snake_body = deque()
        self.food_position = ()
        self.game_over = False

    def reset(self):
        self.score = 0
        self.speed = 1
        self.snake_body.clear()
        self.snake_body.append((self.width // 2, self.height // 2))
        self.food_position = self.generate_food_position()
        self.game_over = False

    def draw(self, window):
        window.draw_border()
        window.draw_text(f"Score: {self.score}", 2, 2)
        window.draw_text(f"High Score: {self.high_score}", 2, 4)
        window.draw_snake(self.snake_body)
        window.draw_food(self.food_position)

    def update(self, window):
        if self.game_over:
            return

        head = self.snake_body[0]
        direction = self.get_direction()
        new_head = self.get_new_head(head, direction)

        if self.collide(new_head):
            self.game_over = True
            return

        self.snake_body.appendleft(new_head)

        if new_head == self.food_position:
            self.score += 1
            self.speed += 0.1
            self.food_position = self.generate_food_position()
        else:
            self.snake_body.pop()

        if self.score > self.high_score:
            self.high_score = self.score

        window.refresh()
        time.sleep(0.1 / self.speed)

    def handle_input(self, key):
        if key == curses.KEY_UP:
            self.set_direction("up")
        elif key == curses.KEY_DOWN:
            self.set_direction("down")
        elif key == curses.KEY_LEFT:
            self.set_direction("left")
        elif key == curses.KEY_RIGHT:
            self.set_direction("right")

    def run(self):
        curses.initscr()
        curses.curs_set(0)
        window = Window(self.width, self.height)

        while True:
            key = window.get_key()
            if key == ord("q"):
                break

            self.handle_input(key)
            self.update(window)

            if self.game_over:
                window.draw_text("Game Over!", self.width // 2 - 4, self.height // 2)
                window.refresh()
                time.sleep(2)
                self.reset()
                window.clear()

        window.close()
        curses.endwin()

    def get_direction(self):
        return self.snake_body[0][2]

    def set_direction(self, direction):
        head = self.snake_body[0]
        self.snake_body[0] = (head[0], head[1], direction)

    def get_new_head(self, head, direction):
        x, y, _ = head

        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1

        return x, y, direction

    def collide(self, head):
        x, y, _ = head

        if x < 1 or x > self.width - 2 or y < 1 or y > self.height - 2:
            return True

        for body_part in self.snake_body[1:]:
            if body_part[:2] == head[:2]:
                return True

        return False

    def generate_food_position(self):
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if (x, y) not in self.snake_body:
                return x, y


class Snake:
    def __init__(self, start_position):
        self.body = deque([start_position])
        self.direction = "right"

    def move(self, direction):
        if direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "right" and self.direction != "left":
            self.direction = "right"

    def eat(self):
        self.body.append(self.body[-1])

    def collide(self, width, height):
        x, y = self.body[0]

        if x < 1 or x > width - 2 or y < 1 or y > height - 2:
            return True

        for body_part in self.body[1:]:
            if body_part == self.body[0]:
                return True

        return False


class Food:
    def __init__(self, width, height):
        self.position = self.generate(width, height)

    def generate(self, snake_body):
        while True:
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            if (x, y) not in snake_body:
                return x, y


class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.window = curses.newwin(height, width, 0, 0)
        self.window.timeout(100)

    def draw_border(self):
        self.window.border()

    def draw_text(self, text, x, y):
        self.window.addstr(y, x, text)

    def draw_snake(self, snake_body):
        for x, y, _ in snake_body:
            self.window.addch(y, x, "*")

    def draw_food(self, food_position):
        x, y = food_position
        self.window.addch(y, x, "+")

    def refresh(self):
        self.window.refresh()

    def get_key(self):
        return self.window.getch()

    def close(self):
        self.window.clear()
        self.window.refresh()
        self.window.getch()
        curses.endwin()


if __name__ == "__main__":
    game = Game(40, 20)
    game.run()
