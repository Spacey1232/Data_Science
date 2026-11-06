import sys
from random import randint

def main(argc, argv):
    class Research():
        class Calculations:
            def __init__(self, data):
                self.data = data
            def counts(self):
                count_orel = 0
                count_res = 0
                for i in self.data:
                    if i[0] == 1:
                        count_orel += 1
                    elif i[0] == 0:
                        count_res += 1
                return count_orel, count_res

            def fractions(self, count_orel, count_res):
                total = count_orel + count_res
                return count_orel / total, count_res / total
        class Analytics(Calculations):
            def predict_random(self, count_numbers):
                predictions = []
                for _ in range(count_numbers):
                    random_value = randint(0, 1)
                    predictions.append([random_value, 1 - random_value])
                return predictions
            def predict_last(self):
                return self.data[-1]

        def __init__(self, path):
            self.path = path

        def file_reader(self, has_header=True):
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

    if argc != 2:
        raise ValueError("Запуск: python3 first_nest.py data.csv")
    reader = Research(argv[1])
    data = reader.file_reader()
    calculation = Research.Calculations(data)
    count_orel, count_res = calculation.counts()
    analytic = Research.Analytics(data)
    print(data)
    print(count_orel, count_res)
    fraction_orel, fraction_res = calculation.fractions(count_orel, count_res)
    print(fraction_orel, fraction_res)
    print(analytic.predict_random(count_orel + count_res))
    print(analytic.predict_last())


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except (ValueError, OSError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)