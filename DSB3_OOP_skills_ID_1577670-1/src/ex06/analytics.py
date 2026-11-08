from random import randint
import json
import urllib.request
import logging
import config


def configure_logging():
    logging.basicConfig(
        filename = "analytics.log",
        level=logging.INFO,
        format="%(asctime)s %(message)s"
    )


class Research():
    class Calculations:
        def __init__(self, data):
            logging.info("Метод __init__ класса Calculations является конструктором(иницилизирует поля обьекта)")
            self.data = data

        def counts(self):
            logging.info("Метод count класса Calculations считает кол-во орлов и решек")

            count_orel = 0
            count_res = 0
            for i in self.data:
                if i[0] == 1:
                    count_orel += 1
                elif i[0] == 0:
                    count_res += 1
            return count_orel, count_res

        def fractions(self, count_orel, count_res):
            logging.info("Метод fractions класса Calculations считает вероятность орла и решек")

            total = count_orel + count_res
            return count_orel / total, count_res / total

    class Analytics(Calculations):
        def predict_random(self, count_numbers):
            logging.info("Метод predict_random класса Analytics возвращает массив с предиктами будет орел или решка")
            predictions = []
            for _ in range(count_numbers):
                random_value = randint(0, 1)
                predictions.append([random_value, 1 - random_value])
            return predictions

        def predict_last(self):
            logging.info("Метод predict_last класса Analytics возвращает последний элемент данных, которые передаются в файле data.csv")
            return self.data[-1]

        def save_file(self, data, filename, extension):
            logging.info("Метод save_file класса Analytics создает и записывает текст")
            full_name = filename + "." + extension
            with open(full_name, "w") as f:
                f.write(str(data))

    def __init__(self, path):
        configure_logging()
        logging.info("Метод __init__ класса Research является конструктор(иницилизирует поля обеькта)")
        self.path = path

    def file_reader(self, has_header=True):
        logging.info("Метод file_reader класса Research возвращает массив массивов с значением, что выпало в файле data.csv")
        with open(self.path) as f:
            text = f.read()
            list_lines = text.splitlines()

            if not list_lines:
                raise ValueError("Файл пустой")

            if has_header:
                if len(list_lines) < 2:
                    raise ValueError("После заголовка должны быть данные")
                header = list_lines[0].split(",")
                if (len(header) != 2):
                    raise ValueError("Заголовок должен содержать два значения")
                if not header[0].strip() or not header[1].strip():
                    raise ValueError("Значения заголовка не могут быть пустыми")
                other = list_lines[1:]
            else:
                other = list_lines
            mass = []
            for i in other:
                line = i.split(",")
                if (len(line) != 2):
                    raise ValueError("Недостаточно кол-во аргументов в строке")
                if ((line[0] == '0' and line[1] == '1') + (line[0] == '1' and line[1] == '0')) == 0:
                    raise ValueError("Не правильный значения строчек")
                mass.append([int(line[0]), int(line[1])])
            return mass
    def send_message(self, message):
        logging.info("метод send_message отправляет сообщение в Telegram")

        if not config.telegram_bot_token:
            raise ValueError("Не задан TELEGRAM_BOT_TOKEN")

        if not config.telegram_chat_id:
            raise ValueError("Не задан TELEGRAM_CHAT_ID")
        url = (
            f"https://api.telegram.org/"
            f"bot{config.telegram_bot_token}/sendMessage"
        )
        payload = {
            "chat_id": config.telegram_chat_id,
            "text": message
        }

        json_data = json.dumps(payload).encode("utf-8")

        http_request = urllib.request.Request(
            url,
            data=json_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(http_request, timeout=10) as response:
            response.read()
