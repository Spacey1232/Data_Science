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



# Tests use fixed HTML and mocked HTTP: no network or five-second waits.
import pytest
from unittest.mock import Mock, patch


@pytest.mark.parametrize("ticker,values", [
    ("MSFT", ("134,249,000", "125,843,000")),
    ("AAPL", ("100", "90")),
    ("NFLX", ("42", "40")),
])
def test_main_total_revenue(ticker, values, capsys):
    cells = "".join(f"<span>{value}</span>" for value in values)
    html = (
        "<section><div><div><span>Total Revenue</span></div>"
        + cells + "</div></section>"
    )
    response = Mock(text=html)
    with patch.object(requests, "get", return_value=response) as get, patch.object(time, "sleep"):
        result = main(3, ["financial.py", ticker, "Total Revenue"])
    assert result == ("Total Revenue", *values)
    assert isinstance(result, tuple)
    assert capsys.readouterr().out.strip() == str(result)
    assert ticker in get.call_args.args[0]
    response.raise_for_status.assert_called_once_with()


@pytest.mark.parametrize("status", [404, 400, 422])
def test_main_invalid_ticker(status):
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError(f"HTTP {status}")
    with patch.object(requests, "get", return_value=response), patch.object(time, "sleep"):
        with pytest.raises(requests.HTTPError):
            main(3, ["financial.py", "INVALID_TICKER", "Total Revenue"])


@pytest.mark.parametrize("argc,argv", [(1, ["financial.py"]), (2, ["financial.py", "MSFT"]), (4, ["financial.py", "MSFT", "Total Revenue", "extra"])])
def test_main_wrong_arguments(argc, argv):
    with patch.object(requests, "get") as get:
        with pytest.raises(ValueError):
            main(argc, argv)
        get.assert_not_called()


@pytest.mark.parametrize("html", ["<html></html>", "<div>Net Income</div>", "<div><div><span>Total Revenue</span></div></div>"])
def test_main_missing_or_empty_field(html):
    with patch.object(requests, "get", return_value=Mock(text=html)), patch.object(time, "sleep"):
        with pytest.raises(RuntimeError):
            main(3, ["financial.py", "MSFT", "Total Revenue"])


@pytest.mark.parametrize("error", [requests.Timeout("timeout"), requests.ConnectionError("offline"), requests.HTTPError("HTTP 503")])
def test_main_network_errors(error):
    with patch.object(requests, "get", side_effect=error), patch.object(time, "sleep"):
        with pytest.raises(type(error)):
            main(3, ["financial.py", "MSFT", "Total Revenue"])


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except (RuntimeError, ValueError, requests.exceptions.RequestException) as error:
        print(
            f"Ошибка: {error}",
            file=sys.stderr,
        )
        sys.exit(1)
