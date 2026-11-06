import os
import subprocess
def main():

    abs_directory = os.path.dirname(os.path.abspath(__file__))
    expected_environment = os.path.join(abs_directory, "kleinega")
    current_environment = os.environ.get("VIRTUAL_ENV")
    if (
    current_environment is None
    or os.path.realpath(current_environment)
    != os.path.realpath(expected_environment)
    ):
        raise RuntimeError(
        f"Activate the correct environment: {expected_environment}"
        )

    packages = ["pytest", "beautifulsoup4"]

    with open("requirments.txt", "w") as requirments:
        requirments.write("\n".join(packages))
    subprocess.run(
        [
            "pip",
            "install",
            "--upgrade",
            "-r",
            "requirments.txt"
        ],
        check=True
    )
    result = subprocess.run(
        ["pip", "freeze"],
        check=True,
        capture_output=True,
        text=True,
    )
    with open("requirements.txt", "w") as requirements:
        requirements.write(result.stdout)
    
if __name__=="__main__":
    try:
        main()
    except (RuntimeError) as error:
        print(f"Error: {error}")
        raise