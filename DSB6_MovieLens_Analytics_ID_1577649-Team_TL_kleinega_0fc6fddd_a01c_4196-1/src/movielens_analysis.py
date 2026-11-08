import json
import os
import re
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import UTC, datetime

import pytest
from bs4 import BeautifulSoup


def split_csv_line(line: str) -> list[str]:
    fields, current = [], []
    in_quotes = False
    index = 0

    while index < len(line):
        char = line[index]

        if char == '"':
            if in_quotes and index + 1 < len(line) and line[index + 1] == '"':
                current.append('"')
                index += 1
            else:
                in_quotes = not in_quotes

        elif char == "," and not in_quotes:
            fields.append("".join(current))
            current = []

        else:
            current.append(char)

        index += 1

    fields.append("".join(current))
    return fields


def read_csv(
    path_to_the_file: str,
    limit: int | None = 1000,
) -> list[list[str]]:
    rows = []

    with open(path_to_the_file, encoding="utf-8") as file:
        next(file, None)

        for index, line in enumerate(file):
            if limit is not None and index >= limit:
                break

            rows.append(
                split_csv_line(
                    line.rstrip("\r\n")
                )
            )

    return rows


def average(values: list[int | float]) -> float:
    return sum(values) / len(values)


def median(values: list[int | float]) -> float:
    ordered = sorted(values)
    middle = len(ordered) // 2

    if len(ordered) % 2:
        return float(ordered[middle])

    return (
        ordered[middle - 1] + ordered[middle]
    ) / 2


def variance(values: list[int | float]) -> float:
    mean = average(values)

    return sum(
        (value - mean) ** 2
        for value in values
    ) / len(values)


def to_number(
    value: str | int | float | None,
) -> int | None:
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return int(value)

    digits = re.sub(
        r"[^0-9]",
        "",
        str(value),
    )

    return int(digits) if digits else None


def runtime_minutes(
    value: str | int | float | None,
) -> int | None:
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return int(value)

    text = str(value)

    match = re.search(
        r"PT(?:(\d+)H)?(?:(\d+)M)?",
        text,
    )

    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)

        return hours * 60 + minutes

    match = re.search(r"\d+", text)

    return int(match.group()) if match else None


class Ratings:
    """Analyzing data from ratings.csv."""

    def __init__(
        self,
        path_to_the_file: str,
    ) -> None:
        self.path = path_to_the_file
        self.data = []

        movies_path = os.path.join(
            os.path.dirname(path_to_the_file),
            "movies.csv",
        )

        titles = {}

        if os.path.exists(movies_path):
            for row in read_csv(
                movies_path,
                limit=None,
            ):
                if len(row) >= 2:
                    titles[int(row[0])] = row[1]

        for row in read_csv(path_to_the_file):
            if len(row) == 4:
                movie_id = int(row[1])

                self.data.append(
                    {
                        "userId": int(row[0]),
                        "movieId": movie_id,
                        "title": titles.get(
                            movie_id,
                            f"Unknown (ID: {movie_id})",
                        ),
                        "rating": float(row[2]),
                        "timestamp": int(row[3]),
                    }
                )

        self.movies = self.Movies(self.data)
        self.users = self.Users(self.data)

    class Movies:
        def __init__(
            self,
            data: list[dict[str, object]],
        ) -> None:
            self.data = data

        def dist_by_year(
            self,
        ) -> dict[int, int]:
            """
            Возвращает распределение оценок по годам.

            Ключ:
                год выставления оценки.

            Значение:
                количество оценок за этот год.
            """
            result = Counter(
                datetime.fromtimestamp(
                    row["timestamp"],
                    tz=UTC,
                ).year
                for row in self.data
            )

            return dict(
                sorted(result.items())
            )

        def dist_by_rating(
            self,
        ) -> dict[float, int]:
            """
            Возвращает распределение оценок.

            Ключ:
                значение оценки.

            Значение:
                количество таких оценок.
            """
            result = Counter(
                row["rating"]
                for row in self.data
            )

            return dict(
                sorted(result.items())
            )

        def top_by_num_of_ratings(
            self,
            n: int,
        ) -> dict[str, int]:
            """
            Возвращает top-n фильмов
            по количеству оценок.

            Ключ:
                название фильма.

            Значение:
                количество оценок.
            """
            counts = Counter(
                row["title"]
                for row in self.data
            )

            result = sorted(
                counts.items(),
                key=lambda item: (
                    -item[1],
                    item[0],
                ),
            )

            return dict(result[:n])

        def top_by_ratings(
            self,
            n: int,
            metric=average,
        ) -> dict[str, float]:
            """
            Возвращает top-n фильмов
            по среднему или медианному рейтингу.

            Ключ:
                название фильма.

            Значение:
                результат функции metric.
            """
            grouped = defaultdict(list)

            for row in self.data:
                grouped[row["title"]].append(
                    row["rating"]
                )

            result = [
                (
                    title,
                    round(metric(values), 2),
                )
                for title, values
                in grouped.items()
            ]

            result.sort(
                key=lambda item: (
                    -item[1],
                    item[0],
                )
            )

            return dict(result[:n])

        def top_controversial(
            self,
            n: int,
        ) -> dict[str, float]:
            """
            Возвращает top-n фильмов
            с наибольшей дисперсией оценок.

            Ключ:
                название фильма.

            Значение:
                дисперсия оценок.
            """
            grouped = defaultdict(list)

            for row in self.data:
                grouped[row["title"]].append(
                    row["rating"]
                )

            result = [
                (
                    title,
                    round(variance(values), 2),
                )
                for title, values
                in grouped.items()
            ]

            result.sort(
                key=lambda item: (
                    -item[1],
                    item[0],
                )
            )

            return dict(result[:n])

    class Users(Movies):
        def dist_by_num_of_ratings(
            self,
        ) -> dict[int, int]:
            """
            Возвращает количество оценок
            каждого пользователя.

            Ключ:
                userId.

            Значение:
                количество оценок.
            """
            result = Counter(
                row["userId"]
                for row in self.data
            )

            return dict(
                sorted(result.items())
            )

        def dist_by_ratings(
            self,
            metric=average,
        ) -> dict[int, float]:
            """
            Возвращает среднюю или медианную
            оценку каждого пользователя.

            Ключ:
                userId.

            Значение:
                результат функции metric.
            """
            grouped = defaultdict(list)

            for row in self.data:
                grouped[row["userId"]].append(
                    row["rating"]
                )

            result = [
                (
                    user_id,
                    round(metric(values), 2),
                )
                for user_id, values
                in grouped.items()
            ]

            return dict(sorted(result))

        def top_controversial(
            self,
            n: int,
        ) -> dict[int, float]:
            """
            Возвращает пользователей
            с наибольшей дисперсией оценок.

            Ключ:
                userId.

            Значение:
                дисперсия оценок.
            """
            grouped = defaultdict(list)

            for row in self.data:
                grouped[row["userId"]].append(
                    row["rating"]
                )

            result = [
                (
                    user_id,
                    round(variance(values), 2),
                )
                for user_id, values
                in grouped.items()
            ]

            result.sort(
                key=lambda item: (
                    -item[1],
                    item[0],
                )
            )

            return dict(result[:n])


class Tags:
    """Analyzing data from tags.csv."""

    def __init__(
        self,
        path_to_the_file: str,
    ) -> None:
        self.path = path_to_the_file
        self.data = []

        for row in read_csv(path_to_the_file):
            if len(row) == 4:
                self.data.append(
                    {
                        "userId": int(row[0]),
                        "movieId": int(row[1]),
                        "tag": row[2],
                        "timestamp": int(row[3]),
                    }
                )

    def most_words(
        self,
        n: int,
    ) -> dict[str, int]:
        """
        Возвращает top-n тегов
        с наибольшим количеством слов.

        Ключ:
            тег.

        Значение:
            количество слов.
        """
        unique = {
            row["tag"]
            for row in self.data
        }

        result = [
            (
                tag,
                len(
                    re.findall(
                        r"\b\w+\b",
                        tag,
                    )
                ),
            )
            for tag in unique
        ]

        result.sort(
            key=lambda item: (
                -item[1],
                item[0],
            )
        )

        return dict(result[:n])

    def longest(
        self,
        n: int,
    ) -> list[str]:
        """
        Возвращает top-n самых длинных
        уникальных тегов.

        Результат:
            список строк.
        """
        unique = {
            row["tag"]
            for row in self.data
        }

        return sorted(
            unique,
            key=lambda tag: (
                -len(tag),
                tag,
            ),
        )[:n]

    def most_words_and_longest(
        self,
        n: int,
    ) -> list[str]:
        """
        Возвращает пересечение между:

        - top-n тегов по количеству слов;
        - top-n тегов по длине.

        Результат:
            список строк.
        """
        most_words_tags = set(
            self.most_words(n)
        )

        longest_tags = set(
            self.longest(n)
        )

        return sorted(
            most_words_tags & longest_tags
        )

    def most_popular(
        self,
        n: int,
    ) -> dict[str, int]:
        """
        Возвращает самые популярные теги.

        Ключ:
            тег.

        Значение:
            количество использований.
        """
        counts = Counter(
            row["tag"]
            for row in self.data
        )

        result = sorted(
            counts.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        return dict(result[:n])

    def tags_with(
        self,
        word: str,
    ) -> list[str]:
        """
        Возвращает уникальные теги,
        содержащие переданное слово.

        Результат:
            список строк по алфавиту.
        """
        word = word.lower()

        return sorted(
            {
                row["tag"]
                for row in self.data
                if word in row["tag"].lower()
            }
        )


class Movies:
    """Analyzing data from movies.csv."""

    def __init__(
        self,
        path_to_the_file: str,
    ) -> None:
        self.path = path_to_the_file
        self.data = []

        for row in read_csv(path_to_the_file):
            if len(row) == 3:
                match = re.search(
                    r"\((\d{4})\)\s*$",
                    row[1],
                )

                if row[2] == "(no genres listed)":
                    genres = []
                else:
                    genres = row[2].split("|")

                self.data.append(
                    {
                        "movieId": int(row[0]),
                        "title": row[1],
                        "year": (
                            int(match.group(1))
                            if match
                            else None
                        ),
                        "genres": genres,
                    }
                )

    def dist_by_release(
        self,
    ) -> dict[int, int]:
        """
        Возвращает распределение фильмов
        по годам выхода.

        Ключ:
            год выхода фильма.

        Значение:
            количество фильмов.
        """
        counts = Counter(
            row["year"]
            for row in self.data
            if row["year"] is not None
        )

        result = sorted(
            counts.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        return dict(result)

    def dist_by_genres(
        self,
    ) -> dict[str, int]:
        """
        Возвращает распределение фильмов
        по жанрам.

        Ключ:
            жанр.

        Значение:
            количество фильмов.
        """
        counts = Counter(
            genre
            for row in self.data
            for genre in row["genres"]
        )

        result = sorted(
            counts.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        return dict(result)

    def most_genres(
        self,
        n: int,
    ) -> dict[str, int]:
        """
        Возвращает top-n фильмов
        с наибольшим количеством жанров.

        Ключ:
            название фильма.

        Значение:
            количество жанров.
        """
        result = [
            (
                row["title"],
                len(row["genres"]),
            )
            for row in self.data
        ]

        result.sort(
            key=lambda item: (
                -item[1],
                item[0],
            )
        )

        return dict(result[:n])


class Links:
    """Analyzing data from links.csv and IMDb."""

    def __init__(
        self,
        path_to_the_file: str,
    ) -> None:
        self.path = path_to_the_file
        self.data = []
        self.imdb_info = []

        movies_path = os.path.join(
            os.path.dirname(path_to_the_file),
            "movies.csv",
        )

        titles = {}

        if os.path.exists(movies_path):
            for row in read_csv(
                movies_path,
                limit=None,
            ):
                if len(row) >= 2:
                    titles[int(row[0])] = row[1]

        for row in read_csv(path_to_the_file):
            if len(row) >= 2:
                movie_id = int(row[0])

                self.data.append(
                    {
                        "movieId": movie_id,
                        "title": titles.get(
                            movie_id,
                            f"Unknown (ID: {movie_id})",
                        ),
                        "imdbId": str(
                            row[1]
                        ).zfill(7),
                        "tmdbId": (
                            row[2]
                            if len(row) > 2
                            and row[2]
                            else None
                        ),
                    }
                )

    def _fetch_imdb(
        self,
        imdb_id: str | int,
    ) -> dict[str, str | int | None]:
        """
        Получает информацию о фильме
        со страницы IMDb.

        Возвращает словарь с полями:

        - Title;
        - Director;
        - Budget;
        - Cumulative Worldwide Gross;
        - Runtime.
        """
        url = (
            "https://www.imdb.com/title/"
            f"tt{str(imdb_id).zfill(7)}/"
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(X11; Linux x86_64)"
                )
            },
        )

        empty = {
            "Title": None,
            "Director": None,
            "Budget": None,
            "Cumulative Worldwide Gross": None,
            "Runtime": None,
        }

        try:
            with urllib.request.urlopen(
                request,
                timeout=15,
            ) as response:
                html = response.read().decode(
                    "utf-8",
                    errors="replace",
                )

        except (
            urllib.error.HTTPError,
            urllib.error.URLError,
            TimeoutError,
        ):
            return empty

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        result = dict(empty)

        scripts = soup.find_all(
            "script",
            attrs={
                "type": "application/ld+json"
            },
        )

        for script in scripts:
            try:
                payload = json.loads(
                    script.string or "{}"
                )

            except (
                json.JSONDecodeError,
                TypeError,
            ):
                continue

            if isinstance(payload, list):
                payload = next(
                    (
                        item
                        for item in payload
                        if isinstance(item, dict)
                    ),
                    {},
                )

            if not isinstance(payload, dict):
                continue

            result["Title"] = payload.get(
                "name"
            )

            result["Runtime"] = runtime_minutes(
                payload.get("duration")
            )

            directors = payload.get("director")

            if isinstance(directors, dict):
                result["Director"] = directors.get(
                    "name"
                )

            elif isinstance(directors, list):
                result["Director"] = (
                    ", ".join(
                        item.get("name", "")
                        for item in directors
                        if (
                            isinstance(item, dict)
                            and item.get("name")
                        )
                    )
                    or None
                )

            break

        if result["Title"] is None:
            title = soup.find("h1")

            result["Title"] = (
                title.get_text(strip=True)
                if title
                else None
            )

        budget = re.search(
            (
                r'"budget"\s*:\s*\{.*?'
                r'"amount"\s*:\s*([0-9]+)'
            ),
            html,
            re.IGNORECASE | re.DOTALL,
        )

        gross = re.search(
            (
                r'"worldwideGross"\s*:\s*\{.*?'
                r'"amount"\s*:\s*([0-9]+)'
            ),
            html,
            re.IGNORECASE | re.DOTALL,
        )

        result["Budget"] = (
            to_number(budget.group(1))
            if budget
            else None
        )

        result[
            "Cumulative Worldwide Gross"
        ] = (
            to_number(gross.group(1))
            if gross
            else None
        )

        return result

    def get_imdb(
        self,
        list_of_movies: list[int],
        list_of_fields: list[str],
    ) -> list[list[object]]:
        """
        Получает поля IMDb для списка movieId.

        Возвращает список списков:

        [
            [movieId, field1, field2, ...],
            ...
        ]

        Результат сортируется по movieId
        по убыванию.
        """
        by_id = {
            row["movieId"]: row
            for row in self.data
        }

        movie_ids = sorted(
            {
                int(value)
                for value in list_of_movies
            },
            reverse=True,
        )

        result = []

        for movie_id in movie_ids:
            link = by_id.get(movie_id)

            if link is None:
                continue

            info = self._fetch_imdb(
                link["imdbId"]
            )

            info["movieId"] = movie_id

            info["Title"] = (
                info.get("Title")
                or link["title"]
            )

            self.imdb_info = [
                row
                for row in self.imdb_info
                if (
                    row.get("movieId")
                    != movie_id
                )
            ]

            self.imdb_info.append(info)

            result.append(
                [movie_id]
                + [
                    info.get(field)
                    for field in list_of_fields
                ]
            )

        self.imdb_info.sort(
            key=lambda row: row["movieId"],
            reverse=True,
        )

        return result

    def top_directors(
        self,
        n: int,
    ) -> dict[str, int]:
        """
        Возвращает top-n режиссёров.

        Ключ:
            имя режиссёра.

        Значение:
            количество фильмов.
        """
        counts = Counter()

        for row in self.imdb_info:
            if row.get("Director"):
                directors = row[
                    "Director"
                ].split(", ")

                for director in directors:
                    counts[director] += 1

        result = sorted(
            counts.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        return dict(result[:n])

    def most_expensive(
        self,
        n: int,
    ) -> dict[str, int]:
        """
        Возвращает top-n фильмов
        с максимальным бюджетом.

        Ключ:
            название фильма.

        Значение:
            бюджет.
        """
        result = [
            (
                row["Title"],
                row["Budget"],
            )
            for row in self.imdb_info
            if (
                row.get("Title")
                and row.get("Budget")
                is not None
            )
        ]

        result.sort(
            key=lambda item: (
                -item[1],
                item[0],
            )
        )

        return dict(result[:n])

    def most_profitable(
        self,
        n: int,
    ) -> dict[str, int]:
        """
        Возвращает top-n самых прибыльных
        фильмов.

        Ключ:
            название фильма.

        Значение:
            мировые сборы минус бюджет.
        """
        result = []

        for row in self.imdb_info:
            budget = row.get("Budget")

            gross = row.get(
                "Cumulative Worldwide Gross"
            )

            if (
                row.get("Title")
                and budget is not None
                and gross is not None
            ):
                result.append(
                    (
                        row["Title"],
                        gross - budget,
                    )
                )

        result.sort(
            key=lambda item: (
                -item[1],
                item[0],
            )
        )

        return dict(result[:n])

    def longest(
        self,
        n: int,
    ) -> dict[str, int]:
        """
        Возвращает top-n самых длинных
        фильмов.

        Ключ:
            название фильма.

        Значение:
            продолжительность в минутах.
        """
        result = [
            (
                row["Title"],
                row["Runtime"],
            )
            for row in self.imdb_info
            if (
                row.get("Title")
                and row.get("Runtime")
                is not None
            )
        ]

        result.sort(
            key=lambda item: (
                -item[1],
                item[0],
            )
        )

        return dict(result[:n])

    def top_cost_per_minute(
        self,
        n: int,
    ) -> dict[str, float]:
        """
        Возвращает top-n фильмов
        по стоимости одной минуты.

        Ключ:
            название фильма.

        Значение:
            бюджет, делённый
            на продолжительность.
        """
        result = []

        for row in self.imdb_info:
            budget = row.get("Budget")
            runtime = row.get("Runtime")

            if (
                row.get("Title")
                and budget is not None
                and runtime
            ):
                result.append(
                    (
                        row["Title"],
                        round(
                            budget / runtime,
                            2,
                        ),
                    )
                )

        result.sort(
            key=lambda item: (
                -item[1],
                item[0],
            )
        )

        return dict(result[:n])


class Tests:
    """PyTest checks for mandatory methods."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        data_directory = os.path.join(
            os.path.dirname(__file__),
            "..",
            "datasets",
            "ml-latest-small",
        )

        self.ratings = Ratings(
            os.path.join(
                data_directory,
                "ratings.csv",
            )
        )

        self.tags = Tags(
            os.path.join(
                data_directory,
                "tags.csv",
            )
        )

        self.movies = Movies(
            os.path.join(
                data_directory,
                "movies.csv",
            )
        )

        self.links = Links(
            os.path.join(
                data_directory,
                "links.csv",
            )
        )

        self.links.imdb_info = [
            {
                "movieId": 1,
                "Title": "Toy Story (1995)",
                "Director": "John Lasseter",
                "Budget": 30000000,
                "Cumulative Worldwide Gross": (
                    394436586
                ),
                "Runtime": 81,
            },
            {
                "movieId": 2,
                "Title": "Jumanji (1995)",
                "Director": "Joe Johnston",
                "Budget": 65000000,
                "Cumulative Worldwide Gross": (
                    262821940
                ),
                "Runtime": 104,
            },
        ]

    def test_ratings_movies(self) -> None:
        assert isinstance(
            self.ratings.movies.dist_by_year(),
            dict,
        )

        assert isinstance(
            self.ratings.movies.dist_by_rating(),
            dict,
        )

        assert isinstance(
            self.ratings.movies.top_by_num_of_ratings(
                5
            ),
            dict,
        )

        assert isinstance(
            self.ratings.movies.top_by_ratings(5),
            dict,
        )

        assert isinstance(
            self.ratings.movies.top_by_ratings(
                5,
                median,
            ),
            dict,
        )

        assert isinstance(
            self.ratings.movies.top_controversial(
                5
            ),
            dict,
        )

        for result in [self.ratings.movies.dist_by_year(), self.ratings.movies.dist_by_rating()]:
            assert list(result) == sorted(result)
            assert all(isinstance(k, (int, float)) and isinstance(v, int) for k, v in result.items())
        for result in [self.ratings.movies.top_by_num_of_ratings(5), self.ratings.movies.top_by_ratings(5), self.ratings.movies.top_by_ratings(5, median), self.ratings.movies.top_controversial(5)]:
            assert all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in result.items())
            assert list(result.values()) == sorted(result.values(), reverse=True)

    def test_ratings_users(self) -> None:
        assert isinstance(
            self.ratings.users.dist_by_num_of_ratings(),
            dict,
        )

        assert isinstance(
            self.ratings.users.dist_by_ratings(),
            dict,
        )

        assert isinstance(
            self.ratings.users.dist_by_ratings(
                median
            ),
            dict,
        )

        assert isinstance(
            self.ratings.users.top_controversial(
                5
            ),
            dict,
        )

        for result in [self.ratings.users.dist_by_num_of_ratings(), self.ratings.users.dist_by_ratings(), self.ratings.users.dist_by_ratings(median)]:
            assert list(result) == sorted(result)
            assert all(isinstance(k, int) and isinstance(v, (int, float)) for k, v in result.items())
        result = self.ratings.users.top_controversial(5)
        assert all(isinstance(k, int) and isinstance(v, float) for k, v in result.items())
        assert list(result.values()) == sorted(result.values(), reverse=True)

    def test_tags(self) -> None:
        assert isinstance(
            self.tags.most_words(5),
            dict,
        )

        assert isinstance(
            self.tags.longest(5),
            list,
        )

        assert isinstance(
            self.tags.most_words_and_longest(5),
            list,
        )

        assert isinstance(
            self.tags.most_popular(5),
            dict,
        )

        assert isinstance(
            self.tags.tags_with("love"),
            list,
        )

        for result in [self.tags.most_words(5), self.tags.most_popular(5)]:
            assert all(isinstance(k, str) and isinstance(v, int) for k, v in result.items())
            assert list(result.values()) == sorted(result.values(), reverse=True)
        longest = self.tags.longest(5)
        assert all(isinstance(tag, str) for tag in longest)
        assert [len(tag) for tag in longest] == sorted([len(tag) for tag in longest], reverse=True)
        intersection = self.tags.most_words_and_longest(5)
        assert all(isinstance(tag, str) for tag in intersection)
        assert set(intersection) == set(self.tags.most_words(5)) & set(longest)
        tags = self.tags.tags_with("love")
        assert all(isinstance(tag, str) and "love" in tag.lower() for tag in tags)
        assert tags == sorted(set(tags))

    def test_movies(self) -> None:
        assert isinstance(
            self.movies.dist_by_release(),
            dict,
        )

        assert isinstance(
            self.movies.dist_by_genres(),
            dict,
        )

        assert isinstance(
            self.movies.most_genres(5),
            dict,
        )

        for result in [self.movies.dist_by_release(), self.movies.dist_by_genres(), self.movies.most_genres(5)]:
            assert all(isinstance(k, (str, int)) and isinstance(v, int) for k, v in result.items())
            assert list(result.values()) == sorted(result.values(), reverse=True)

    def test_links_get_imdb(
        self,
        monkeypatch,
    ) -> None:
        def fake_fetch(
            _imdb_id: str | int,
        ) -> dict[str, str | int | None]:
            return {
                "Title": "Movie",
                "Director": "Director",
                "Budget": 100,
                "Cumulative Worldwide Gross": 300,
                "Runtime": 10,
            }

        monkeypatch.setattr(
            self.links,
            "_fetch_imdb",
            fake_fetch,
        )

        result = self.links.get_imdb(
            [1, 2],
            [
                "Director",
                "Budget",
            ],
        )

        assert isinstance(result, list)
        assert result[0][0] > result[1][0]

        assert all(isinstance(row, list) and len(row) == 3 for row in result)
        assert all(isinstance(row[0], int) and isinstance(row[1], str) and isinstance(row[2], int) for row in result)
        assert [row[0] for row in result] == sorted([row[0] for row in result], reverse=True)

    def test_links_analytics(self) -> None:
        assert isinstance(
            self.links.top_directors(5),
            dict,
        )

        assert isinstance(
            self.links.most_expensive(5),
            dict,
        )

        assert isinstance(
            self.links.most_profitable(5),
            dict,
        )

        assert isinstance(
            self.links.longest(5),
            dict,
        )

        assert isinstance(
            self.links.top_cost_per_minute(5),
            dict,
        )

        for result in [self.links.top_directors(5), self.links.most_expensive(5), self.links.most_profitable(5), self.links.longest(5), self.links.top_cost_per_minute(5)]:
            assert all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in result.items())
            assert list(result.values()) == sorted(result.values(), reverse=True)


if __name__ == "__main__":
    pass