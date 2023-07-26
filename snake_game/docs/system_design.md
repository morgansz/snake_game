## Implementation approach:
To implement the CLI snake game, we will use the following open-source tools:

1. `curses` library: This library provides a terminal-independent way of creating text-based interfaces. It will be used to handle keyboard input and display the game screen.

2. `random` module: This module will be used to generate random positions for the food in the game.

3. `time` module: This module will be used to control the speed of the game by introducing delays between each frame.

4. `collections` module: This module will be used to implement the snake's body as a deque (double-ended queue) data structure, allowing for efficient insertion and removal of elements.

5. `sys` module: This module will be used to handle system-specific parameters and functions, such as exiting the game.

## Python package name:
```python
"snake_game"
```

## File list:
```python
[
    "main.py",
]
```

## Data structures and interface definitions:
```mermaid
classDiagram
    class Game {
        -int score
        -int high_score
        -int speed
        -int width
        -int height
        -deque snake_body
        -tuple food_position
        -bool game_over
        +__init__(self, width: int, height: int)
        +reset(self)
        +draw(self, window)
        +update(self, window)
        +handle_input(self, key)
        +run(self)
    }

    class Snake {
        -deque body
        -str direction
        +__init__(self, start_position)
        +move(self, direction)
        +eat(self)
        +collide(self, width, height)
    }

    class Food {
        -tuple position
        +__init__(self, width, height)
        +generate(self, snake_body)
    }

    class Window {
        -int width
        -int height
        -curses window
        +__init__(self, width: int, height: int)
        +draw_border(self)
        +draw_text(self, text, x, y)
        +draw_snake(self, snake_body)
        +draw_food(self, food_position)
        +refresh(self)
        +close(self)
    }

    Game "1" -- "1" Snake: has
    Game "1" -- "1" Food: has
    Game "1" -- "1" Window: uses
    Snake "1" -- "1" Food: eats
    Window "1" -- "1" curses: uses
```

## Program call flow:
```mermaid
sequenceDiagram
    participant M as Main
    participant G as Game
    participant W as Window
    participant S as Snake
    participant F as Food

    M->>G: Create game instance with specified width and height
    G->>W: Create window instance with specified width and height
    G->>G: Reset game state
    G->>W: Draw game screen
    G->>W: Refresh window
    loop
        M->>G: Get user input
        G->>G: Handle input
        G->>G: Update game state
        G->>W: Draw game screen
        G->>W: Refresh window
    end
    G->>W: Close window
```

## Anything UNCLEAR:
The requirements and design are clear to me.