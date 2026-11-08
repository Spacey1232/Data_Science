#!/usr/bin/env python3

import timeit


def base_method(emails):
    result = []
    for email in emails:
        if "@gmail" in email:
            result.append(email)
    return result


def senond_variant(emails):
    result = [
        email
        for email in emails
        if "@gmail" in email
    ]
    return result


def third_variant(emails):
    result = map(
        lambda email: (
            email if "@gmail" in email else None
        ),
        emails,
    )
    return result


def main():
    emails = [
        "john@gmail.com",
        "james@gmail.com",
        "alice@yahoo.com",
        "anna@live.com",
        "philipp@gmail.com",
    ] * 5

    time1 = timeit.timeit(
        lambda: base_method(emails),
        number=90_000_000,
    )

    time2 = timeit.timeit(
        lambda: senond_variant(emails),
        number=90_000_000,
    )

    time3 = timeit.timeit(
        lambda: third_variant(emails),
        number=90_000_000,
    )

    min_time = min(time1, time2, time3)

    if time2 == min_time:
        print("it is better to use a list comprehension")
    elif time1 == min_time:
        print("it is better to use a loop")
    else:
        print("it is better to use a map")

    result = sorted([time1, time2, time3])

    print(result[0], "vs", result[1], "vs", result[2])



if __name__ == "__main__":
    main()