Game bots
================
Персональные боты для игр, реализованные через компьютерное зрение OpenCV. 
#### Основные возможности
- Поиск заданных изображений на экране и реализация логики при появления изображения на экране 
- Настройка логики при отсутствии активности в течение N секунд (например, вылет из игры)
- Выведение экрана с игрой на главный план после запуска бота

Модуль с ботом - bot_runner.py

#### Пример запуска
```
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
```
