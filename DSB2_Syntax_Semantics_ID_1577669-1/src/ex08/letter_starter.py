import sys


def main(argc, argv):
    if argc != 2:
        return

    with open("employees.tsv", "r") as f:
        f.readline()

        for line in f:
            data = line.strip().split("\t")
            name = data[0]
            email = data[2]

            if argv[1] == email:
                print(
                    f"{name}, добро пожаловать в нашу команду! "
                    "Мы уверены, что работать вместе с тобой будет очень приятно. "
                    "Для нас это важно — мы стремимся, чтобы в компании "
                    "работали именно такие люди."
                )
if __name__ == "__main__":
    main(len(sys.argv), sys.argv)