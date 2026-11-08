# Data Science — проекты Школы 21

Мои учебные проекты по Python и анализу данных. Каждый проект находится в отдельной папке с исходным школьным названием. Решения расположены в `src`, примеры из заданий — в `code-samples`, входные данные и материалы — в соответствующих каталогах проектов.

## Проекты

| Проект | Технологии | Содержание |
|---|---|---|
| [DSB1 — UNIX Command Line Tools](DSB1_UNIX_Command_Line_Tools_ID_1577674-1/) | Shell, jq, CSV | Получение и преобразование данных о вакансиях, сортировка, выделение позиций, частоты и разбиение по датам. |
| [DSB2 — Python: Syntax and Semantics](DSB2_Syntax_Semantics_ID_1577669-1/) | Python | Типы данных, файлы CSV/TSV, словари, множества, строки, аргументы командной строки и шифр Цезаря. |
| [DSB3 — Python: OOP Skills](DSB3_OOP_skills_ID_1577670-1/) | Python, ООП, logging | Классы и наследование, проверка входных данных, расчёты по подбрасыванию монеты, отчёт и уведомления. |
| [DSB4 — Python: Package Management](DSB4_Package_management_ID_1577671-1/) | venv, requests, httpx, BeautifulSoup, PyTest | Управление пакетами, терминальная диаграмма, финансовый парсер, профилирование и модульные тесты. |
| [DSB5 — Efficient Code Practices](DSB5_Efficient_code_practices_ID_1577672-1/) | timeit, map/filter, reduce, Counter, resource | Эксперименты со временем выполнения и памятью, стандартные инструменты и генераторы. |
| [DSB6 — MovieLens Analytics](DSB6_MovieLens_Analytics_ID_1577649-Team_TL_kleinega_0fc6fddd_a01c_4196-1/) | Python, Jupyter, BeautifulSoup, PyTest | Анализ фильмов, рейтингов и тегов, сбор данных IMDb и аналитический отчёт. |
| [DSB7 — Pandas](DSB7_Pandas_ID_1577650-1/) | Pandas, NumPy, Jupyter | Загрузка и очистка данных, выборки, агрегации, объединения, сводные таблицы и оптимизация DataFrame. |
| [DSB8 — SQL and Pandas](DSB8_SQL_Pandas_ID_1577673-1/) | SQLite, Pandas, Jupyter | SQL-выборки и подзапросы, JOIN, витрина данных, агрегации и сравнение групп. |

## Окружение

Для проверки использован Python 3.13 на macOS. UNIX-упражнениям нужны `jq` и стандартные командные утилиты. Остальные зависимости можно установить в локальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas numpy requests httpx beautifulsoup4 pytest notebook termgraph
```

Виртуальное окружение создаётся на компьютере пользователя и не хранится в Git. DSB4/ex02 использует своё окружение `kleinega`, как предусмотрено заданием. Для DSB2, DSB3 и DSB5 достаточно стандартной библиотеки Python.

Команды ниже выполняются из корня репозитория. Маска `DSB1_*`, например, обозначает единственную папку первого проекта.

## Запуск

### DSB1 — UNIX

```bash
cd DSB1_*/src/ex01
./json_to_csv.sh
cd ../ex02
./sorter.sh
cd ../ex03
./cleaner.sh
cd ../ex04
./counter.sh
cd ../ex05
./partitioner.sh ../ex03/hh_positions.csv
./concatenator.sh 20*.csv
cd ../../..
```

В ex00 включён JSON из задания. После объединения партиций `final.csv` совпадает с `hh_positions.csv`.

### DSB2 — основы Python

```bash
python DSB2_*/src/ex00/data_types.py
python DSB2_*/src/ex02/stock_prices.py tesla
python DSB2_*/src/ex03/ticker_symbols.py tsla
python DSB2_*/src/ex05/all_stocks.py 'TSLA, Apple, unknown'
python DSB2_*/src/ex09/caesar.py encode 'Hello, world!' 3
```

Файловые упражнения запускаются из своих каталогов. В ex01 нужен `ds.csv` из задания. В ex08 `names_extractor.py` принимает путь к файлу адресов `name.surname@corp.com`, создаёт `employees.tsv`; `letter_starter.py` принимает email и формирует приветствие. Цены акций — учебные константы, не текущие котировки.

### DSB3 — ООП

```bash
cd DSB3_*/src/ex05
python make_report.py
cat report.txt
cd ../../..
```

В упражнения включён `data.csv` из условия. Путь к данным, число случайных наблюдений и шаблон отчёта задаются в `config.py`. В ex06 каждый метод пишет в `analytics.log`, а `send_message()` отправляет уведомление о результате в Telegram. Для запуска ex06 нужны собственные переменные `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`. Токен не следует сохранять в Git.

### DSB4 — пакеты, профилирование и тесты

```bash
python DSB4_*/src/ex03/financial.py MSFT 'Total Revenue'
cd DSB4_*/src/ex05
python -m pytest financial_test.py -q
cd ../../..
```

`ex03/financial.py` содержит требуемую паузу 5 секунд. В ex04 версия без паузы использует requests, а `financial_enhanced.py` — httpx. Результаты cProfile и pstats находятся в текстовых файлах ex04. Доступность и разметка Yahoo Finance зависят от внешнего сервиса. В ex05 скрипт и три требуемых теста находятся в одном `financial_test.py`; тестовые HTTP-ответы подменяются, чтобы проверка логики не зависела от сети.

Для упражнения ex02 создай отдельное окружение с нужным именем:

```bash
cd DSB4_*/src/ex02
python3 -m venv kleinega
source kleinega/bin/activate
python librarian.py
deactivate
cd ../../..
source .venv/bin/activate
```

`librarian.py` устанавливает библиотеки через requirements, печатает и сохраняет список установленных версий в `requirements.txt`, создаёт архив окружения. Само окружение и архив создаются локально. Диаграмма ex01 запускается командой `sh pies_bars.sh` из каталога ex01.

### DSB5 — эффективность кода

```bash
python DSB5_*/src/ex02/benchmark.py loop 1000
python DSB5_*/src/ex02/benchmark.py map 1000
python DSB5_*/src/ex03/benchmark.py reduce 1000 100
python DSB5_*/src/ex04/benchmark.py
python DSB5_*/src/ex05/generator.py /путь/к/ratings.csv
```

ex00/ex01 используют заданные в условии 90 миллионов повторений: выполнение может быть долгим. Упражнения с map/filter демонстрируют ленивые итераторы; их создание и вычисление готового списка — разные операции. В ex05 `ordinary.py` загружает строки в список, `generator.py` читает их последовательно; оба выводят пиковую память и время CPU.

### DSB6 — MovieLens

```bash
cd DSB6_*/src
python -m pytest movielens_analysis.py::Tests -q
python -m notebook movielens_report.ipynb
```

В `movielens_analysis.py` находятся требуемые классы `Ratings`, `Tags`, `Movies`, `Links` и `Tests`. Отчёт использует этот модуль. CSV-файлы расположены в `datasets/ml-latest-small`; условия использования данных сохранены в исходном `README.txt` датасета. Для анализа читаются первые 1000 записей. Получение метрик IMDb зависит от доступа к сайту; недоступные поля не заменяются вымышленными значениями.

Проект командный: я написал исходную реализацию всех методов, затем мы с напарником совместно исправляли и дорабатывали код по техническому заданию.

### DSB7 и DSB8 — Pandas и SQL

Открой Jupyter из корня репозитория:

```bash
python -m notebook
```

Выполняй ноутбуки каждого проекта по порядку, с ex00. Рабочим каталогом ядра должен быть каталог открытого ноутбука. Входные данные включены в `src/data`.

В DSB7 ex02 создаёт `auto.json`, ex04 — `fines.csv` и `owners.csv`, ex05 использует полученные данные для замеров. Определения функций отделены от ячеек измерения их вызовов.

В DSB8 ex02 пересоздаёт аналитические таблицы `datamart`, `test` и `control` в рабочей SQLite-базе. Они используются следующими упражнениями. Вывод ex04 описывает наблюдаемое изменение средних в группах; он не приравнивает его к доказанному причинному эффекту.
