#!/usr/bin/env python3

import sys
import resource


def read_file(url):
    with open(url) as file:
        for line in file:
            yield line


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError(
                "Нужно передать путь к файлу"
            )

        file_path = sys.argv[1]
        lines = read_file(file_path)

        for line in lines:
            pass

    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    usage = resource.getrusage(resource.RUSAGE_SELF)
    memory_gb = usage.ru_maxrss / (1024 ** 3)


    cpu_time = usage.ru_utime + usage.ru_stime

    print(f"Peak Memory Usage = {memory_gb:.3f} GB")
    print(
        "User Mode Time + System Mode Time "
        f"= {cpu_time:.2f}s"
    )