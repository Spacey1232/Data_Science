#!/usr/bin/env python3

import sys
import resource

def read_file(url):
    m=[]
    with open(url) as f:
        for line in f:
            m.append(line)
    return m

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Нужно передать путь к файлу")
        lines = read_file(sys.argv[1])
        for line in lines:
            pass
        usage = resource.getrusage(resource.RUSAGE_SELF)
        memory_gb = usage.ru_maxrss / ((1024 ** 3) if sys.platform == "darwin" else (1024 ** 2))
        cpu_time = usage.ru_utime + usage.ru_stime
        print(f"Peak Memory Usage = {memory_gb:.3f} GB")
        print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
