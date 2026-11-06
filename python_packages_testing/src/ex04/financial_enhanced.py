#!/usr/bin/env python3

import sys
import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


def main(argc, argv):
    if argc != 3:
        raise ValueError(
            "Неправильное количество аргументов "
            "передано в командную строку"
        )

    ticker = argv[1].strip().upper()
    field_name = argv[2].strip()


    safe_ticker = quote(ticker, safe="")

    url = (
        f"https://finance.yahoo.com/quote/"
        f"{safe_ticker}/financials"
    )

    params = {
        "p": ticker,
    }

    headers = {
        "Accept": "text/html",
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    field_element = soup.find(
        string=lambda text: (
            text is not None
            and text.strip() == field_name
        )
    )

    if field_element is None:
        raise RuntimeError(
            f"Поле {field_name!r} не найдено"
        )

    current_element = (
        field_element
        .parent
        .parent
        .parent
    )

    values = list(
        current_element.stripped_strings
    )

    if (
        len(values) <= 1
        or values[0] != field_name
    ):
        raise RuntimeError(
            f"Не удалось получить значения "
            f"для поля {field_name!r}"
        )

    result = tuple(values)

    print(result)
    return result


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except (RuntimeError, ValueError, requests.exceptions.RequestException) as error:
        print(
            f"Ошибка: {error}",
            file=sys.stderr,
        )
        sys.exit(1)