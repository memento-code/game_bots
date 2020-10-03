import pyautogui
import time
import random
from functools import partial
from bot_runner import BotRunner


def quite_game():
    pyautogui.keyDown('esc')
    time.sleep(random.randint(1, 10) / 10)
    pyautogui.keyDown('space')
    time.sleep(7)


def continue_game(key, time_sleep):
    pyautogui.keyDown(key)
    time.sleep(time_sleep)


if __name__ == "__main__":
    """
    Автоматический поиск матча, афк во время игры, выход из матча сразу же после окончания и скип окна 
    с результатами матча. 
    """
    actions = [
        {'image': r'drawable\FallGuys\start_image.png', 'action': partial(continue_game, 'space', 180)},
        {'image': r'drawable\FallGuys\result_game.png', 'action': partial(continue_game, 'space', random.randint(1, 10))},
        {'image': r'drawable\FallGuys\end_game_1.png', 'action': quite_game},
        {'image': r'drawable\FallGuys\end_game_2.png', 'action': quite_game}
    ]

    bot = BotRunner(
        inactive_logic={'action': quite_game, 'inactive_seconds': 600},
        frame_time=0.5,
        min_ratio_match=0.8,
        game_logic=actions,
        game_window_name='FallGuys'
    )
    bot.run()
