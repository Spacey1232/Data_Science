#!/usr/bin/env python3

import timeit
import sys


def loop1(emails):
    result = []
    for email in emails:
        if "@gmail" in email:
            result.append(email)
    return result


def list_compehension1(emails):
    result = [
        email
        for email in emails
        if "@gmail" in email
    ]
    return result


def map1(emails):
    result = map(
        lambda email: (
            email if "@gmail" in email else None
        ),
        emails,
    )
    return result

def filter1(emails):
    return filter(
        lambda email: "@gmail.com" in email,
        emails
    )

def main(argc, argv):
    emails = [
            "john@gmail.com",
            "james@gmail.com",
            "alice@yahoo.com",
            "anna@live.com",
            "philipp@gmail.com",
        ] * 5
    if argc == 1:
        return
    if argc != 3:
        raise ValueError(f"Введено не правильно кол-во аргументов в консоли")
    func = argv[1]
    count = int(argv[2])
    if count < 1:
        raise ValueError(f"Введено кол-во повторений ф-ции меньше 1 раза: {count}")
    if func == "loop":
        time = timeit.timeit(
            lambda: loop1(emails),
            number=count
        )
    elif func == "list_comprehension":
        time = timeit.timeit(
            lambda: list_compehension1(emails),
            number=count
        )
    elif func == "map":
        time = timeit.timeit(
            lambda: map1(emails),
            number=count
        )
    elif func == "filter":
        time = timeit.timeit(
            lambda: filter1(emails),
            number=count
        )
    else:
        raise ValueError(f"Введено не существующая ф-ция: {func}")
    print(time)


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except ValueError as error:
        print(f"Ошибка: {error}")
        sys.exit(1)
