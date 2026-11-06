#!/usr/bin/env python3

import sys
import resource

def read_file(url):
    m=[]
    with open(url) as f:
        for line in f:
            m.append(line)
    return m

if __name__=="__main__":
    if len(sys.argv) != 2:
        raise ValueError("Необходимо передать путь к файлу")
    file_path = sys.argv[1]
    lines = read_file(file_path)
    for line in lines:
        pass
    usage = resource.getrusage(resource.RUSAGE_SELF)
    cpu_time = usage.ru_stime + usage.ru_utime
    memory_gb = usage.ru_maxrss / (1024 ** 3)
    print(
        "User Mode Time + System Mode Time"
        f"= {cpu_time:.2f}s"
    )
    print(f"Peak Memory Usage = {memory_gb:.3f} GB")