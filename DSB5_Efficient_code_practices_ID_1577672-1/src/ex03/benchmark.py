#!/usr/bin/env python3

import sys
import timeit
from functools import reduce

def loop1(count):
    summ=0
    for i in range(1, count + 1):
        summ+=i*i
    return summ
def reduce1(count):
    summ = reduce(
        lambda summ, i: summ + i * i,
        range(1, count + 1),
        0
    )
    return summ
def main(argc,argv):
    if argc != 4:
        raise ValueError(f"Введено не правильноe кол-во аргументов в консоли")
    func = argv[1]
    count = int(argv[2])
    rangee=int(argv[3])
    if count < 1:
        raise ValueError(f"Введено кол-во повторений ф-ции меньше 1 раза: {count}")
    if rangee < 1:
        raise ValueError(f"Введен диапазон меньше 1 раза: {rangee}")
    if func == "loop":
        time = timeit.timeit(
            lambda: loop1(rangee),
            number=count
        )
    elif func == "reduce":
        time = timeit.timeit(
            lambda: reduce1(rangee),
            number=count
        )
    else:
        raise ValueError(f"Введено не существующая ф-ция: {func}")
    print(time)

if __name__=="__main__":
    try:
        main(len(sys.argv),sys.argv)
    except ValueError as error:
        print(f"Ошибка: {error}")
        sys.exit(1)