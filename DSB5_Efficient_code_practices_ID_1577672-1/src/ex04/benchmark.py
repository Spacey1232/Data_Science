#!/usr/bin/env python3

import timeit
import random
from collections import Counter


def withoutCounter(array):
    result = {}

    for number in array:
        if number in result:
            result[number] += 1
        else:
            result[number] = 1

    return result


def Counter1(array):
    result = Counter(array)
    return result


def topWithCounter(array):
    dictt = Counter1(array)
    return dict(dictt.most_common(10))


def topWithoutCounter(array):
    result = sorted(
        withoutCounter(array).items(),
        key=lambda part: part[1],
        reverse=True,
    )[:10]

    return dict(result)


def main():
    array = [
        random.randint(0, 100)
        for _ in range(1_000_000)
    ]

    timem = timeit.timeit(
        lambda: withoutCounter(array),
        number=1,
    )

    timeC = timeit.timeit(
        lambda: Counter1(array),
        number=1,
    )

    timemtp = timeit.timeit(
        lambda: topWithoutCounter(array),
        number=1,
    )

    timectp = timeit.timeit(
        lambda: topWithCounter(array),
        number=1,
    )

    print(f"my function: {timem}")
    print(f"Counter: {timeC}")
    print(f"my top: {timemtp}")
    print(f"Counter's top: {timectp}")

if __name__ == "__main__":
    main()