from datetime import datetime
import time
import re
import logging
import numpy
import mss
import win32api
import win32gui
import cv2

logging.basicConfig(filename='bot_runner.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class BotRunner:
    r"""
    Бот для совершения действий при появлении заданных условий на экране. Использует компьютерное зрение для
    сравнения изображения на экране с заданными изображениями. При нахождении изображения на экране - вызывает
    переданную функцию.

    Если в передаваемой функции необходимо также передавать аргументы, то её следует обернуть в partial

    Args:
        inactive_logic(dict) - словарь с логикой при отсутствия активности в течение заданного времени. Ключи:
            - action(fun) - функция, которая будет запущена при отсутствии активности
            - inactive_seconds(int) - время в секундах, после которого необходимо выполнить действие
            - time_sleep(int) - необязательный параметр. Кол-во секунд для ожидания после выполнения действия
        frame_time(int) - время в секундах между повторами проверки изображения с экрана
        min_ratio_match(float) - коэффициент от 0 до 1, используемый для сравнения экрана с заданным изображением
        game_logic(list(dict)) - список с путями изображений и действиями, необходимыми для выполнения
            Формат данных: [{'image': r'drawable\image.png', 'action': func}, ... ]
        game_window_name(str) - название окна с игрой для выведения его его на экран после запуска бота.

    Examples:
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
    """

    def __init__(self, inactive_logic, frame_time, min_ratio_match, game_logic, game_window_name=None):
        self.inactive_logic = inactive_logic
        self.frame_time = frame_time
        self.min_ratio_match = min_ratio_match
        self.game_window_name = game_window_name
        self.game_logic = game_logic
        self._handle_game_window = None
        self.monitor = {'top': 0,
                        'left': 0,
                        'width': win32api.GetSystemMetrics(0),
                        'height': win32api.GetSystemMetrics(1)}

    def _check_image_on_screen(self, screen_img, search_img):
        search_img_cv = cv2.imread(search_img, cv2.IMREAD_GRAYSCALE)
        res = cv2.matchTemplate(screen_img, search_img_cv, cv2.TM_CCOEFF_NORMED)
        loc = numpy.where(res >= self.min_ratio_match)
        return len(loc[0]) > 0

    def _window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle_game_window = hwnd

    def set_foreground(self, game_window_name):
        """
        Выведение игры на главный план по части её названия (например, FallGuys найдёт окно FallGuys_client)
        :param game_window_name: - название игры, которая выведется на главный план
        """
        if game_window_name is not None:
            win32gui.EnumWindows(self._window_enum_callback, game_window_name)
            win32gui.SetForegroundWindow(self._handle_game_window)

    def run(self):
        """Запуск бота через бесконечный цикл"""
        last_update = datetime.now()

        if self.game_logic is None or len(self.game_logic) == 0:
            raise ValueError("Need at least one action for bot")

        with mss.mss() as sct:
            self.set_foreground(self.game_window_name)

            while True:
                img = numpy.array(sct.grab(self.monitor))
                screen_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                for data in self.game_logic:
                    if self._check_image_on_screen(screen_frame, data.get('image')):
                        func = data.get('action')
                        logging.info('Find match with image %s, start function', data.get("image"))
                        func()
                        last_update = datetime.now()

                if (datetime.now() - last_update).seconds > self.inactive_logic.get('inactive_seconds'):
                    logging.warning("No activity since %s", last_update.strftime('%Y-%m-%d %H:%M:%S'))
                    inactive_func = self.inactive_logic.get('action')
                    inactive_func()
                    time.sleep(self.inactive_logic.get('time_sleep', 60))

                if cv2.waitKey(15) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()

                time.sleep(self.frame_time)
