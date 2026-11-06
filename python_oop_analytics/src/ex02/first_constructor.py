import os, sys

def main(argc, argv):
    class Research():
        def __init__(self, path):
            self.path = path
        def file_reader(self):
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"Файл не найден: {self.path}")
            if not os.path.isfile(self.path):
                raise ValueError(f"Указанный путь не является файлом: {self.path}")
            if not os.access(self.path, os.R_OK):
                raise PermissionError(f"Нет прав на чтение файла: {self.path}")
            with open(self.path) as f:
                text = f.read()
                list_lines = text.splitlines()
                if (len(list_lines) < 2):
                    raise ValueError("Недостаточно кол-во строк в файле")
                header = list_lines[0].split(",")
                if (len(header) != 2):
                    raise ValueError("Заголовок должен содержать два значения")
                if not header[0].strip() or not header[1].strip():
                    raise ValueError("Значения заголовка не могут быть пустыми")
                other = list_lines[1:]
                for i in other:
                    line = i.split(",")
                    if (len(line) != 2):
                        raise ValueError("Недостаточно кол-во аргументов в строке")
                    if ((line[0] == '0' and line[1] == '1') + (line[0] == '1' and line[1] == '0')) == 0:
                        raise ValueError("Не правильный значения строчек")
                return text
    if len(argv) != 2:
        raise ValueError("Запуск: python3 first_constructor.py data.csv")
    reader = Research(argv[1])
    print(reader.file_reader())
if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except (ValueError, OSError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)