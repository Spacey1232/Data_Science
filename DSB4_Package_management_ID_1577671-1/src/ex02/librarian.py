#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil


def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    expected = os.path.join(directory, "kleinega")
    if sys.prefix == sys.base_prefix or os.path.realpath(sys.prefix) != os.path.realpath(expected):
        raise RuntimeError(f"Activate the correct environment: {expected}")
    requirements = os.path.join(directory, "requirements.txt")
    with open(requirements, "w") as file:
        file.write("beautifulsoup4\npytest\n")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-r", requirements], check=True)
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], check=True, capture_output=True, text=True)
    print(result.stdout, end="")
    with open(requirements, "w") as file:
        file.write(result.stdout)
    shutil.make_archive(os.path.join(directory, "kleinega"), "zip", directory, "kleinega")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
