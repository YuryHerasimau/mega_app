import torch as t
from torch import tensor as T
from numpy import unravel_index as unravel
import matplotlib.pyplot as plt


def do(snake: t.Tensor, action: int):
    """Based on the article https://habr.com/ru/articles/809997/"""

    positions = snake.flatten().topk(2)[1]
    [pos_cur, pos_prev] = [T(unravel(x, snake.shape)) for x in positions]
    rotation = T([[0, -1], [1, 0]]).matrix_power(3 + action)
    pos_next = (pos_cur + (pos_cur - pos_prev) @ rotation) % T(snake.shape)

    if (snake[tuple(pos_next)] > 0).any():
        return (snake[tuple(pos_cur)] - 2).item()

    if snake[tuple(pos_next)] == -1:
        pos_food = (snake == 0).flatten().to(t.float).multinomial(1)[0]
        snake[unravel(pos_food, snake.shape)] = -1
    else:
        snake[snake > 0] -= 1

    snake[tuple(pos_next)] = snake[tuple(pos_cur)] + 1


def play():
    snake = t.zeros((32, 32), dtype=t.int)
    snake[0, :3] = T([1, 2, -1])

    fig, ax = plt.subplots(1, 1)
    img = ax.imshow(snake)
    action = {"val": 1}
    action_dict = {"a": 0, "d": 2}

    plt.suptitle("PLAY SNAKE!")
    plt.title("To move LEFT and RIGHT use buttons A and D")
    fig.canvas.mpl_connect(
        "key_press_event", lambda e: action.__setitem__("val", action_dict[e.key])
    )

    score = None
    while score is None:
        img.set_data(snake)
        fig.canvas.draw_idle()
        plt.pause(0.1)
        score = do(snake, action["val"])
        action["val"] = 1

    print("Score:", score)
    return f"Game Over! Your Score: {score}"
