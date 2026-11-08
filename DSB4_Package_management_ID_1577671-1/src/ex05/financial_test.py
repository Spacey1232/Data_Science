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

    time.sleep(5)

    safe_ticker = quote(
        ticker,
        safe="",
    )

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

    current_element = field_element.parent
    values = []
    while current_element is not None:
        values = list(current_element.stripped_strings)
        if len(values) > 1 and values[0] == field_name:
            break
        current_element = current_element.parent
    if current_element is None:
        raise RuntimeError(f"Не удалось получить значения для поля {field_name!r}")

    result = tuple(values)

    print(result)

    return result



import pytest
from unittest.mock import Mock


@pytest.fixture
def total_revenue_result(monkeypatch):
    response = Mock(text='<div><div><span>Total Revenue</span></div><span>100</span><span>90</span></div>')
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: response)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    return main(3, ["financial.py", "MSFT", "Total Revenue"])


def test_total_revenue_for_ticker(total_revenue_result):
    assert total_revenue_result == ("Total Revenue", "100", "90")


def test_returned_value_is_tuple(total_revenue_result):
    assert isinstance(total_revenue_result, tuple)


def test_invalid_ticker_raises_exception(monkeypatch):
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("404: invalid ticker")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: response)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    with pytest.raises(requests.HTTPError):
        main(3, ["financial.py", "INVALID_TICKER_123456789", "Total Revenue"])


if __name__ == "__main__":
    try:
        main(
            len(sys.argv),
            sys.argv,
        )
    except (
        RuntimeError,
        ValueError,
        requests.exceptions.RequestException,
    ) as error:
        print(
            f"Ошибка: {error}",
            file=sys.stderr,
        )
        sys.exit(1)