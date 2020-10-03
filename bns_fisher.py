from playsound import playsound
from functools import partial
from bot_runner import BotRunner

if __name__ == "__main__":
    """
    Поиск кнопки вытягивания удочки, звуковое оповещение при нахождении
    """
    actions = [{'image': r'drawable\BnS\fisher_button.png',
                'action': partial(playsound, r'drawable\sounds\mario_coin.mp3')}]
    bot = BotRunner(
        inactive_logic={'action': partial(playsound, r'drawable\sounds\fail.mp3'),
                        'inactive_seconds': 300,
                        'time_sleep': 180},
        frame_time=1,
        min_ratio_match=0.9,
        game_logic=actions,
        game_window_name='Blade & Soul'
    )
    bot.run()
