import sys

def work_files(f, f1):
    f1.write("Name\tSurname\tEmail\n")
    for line in f:
        line = line.strip()
        name = ((line.split("@"))[0].split(".")[0]).capitalize()
        sname = ((line.split("@"))[0].split(".")[1]).capitalize()
        f1.write(f"{name}\t{sname}\t{line}\n")


def main(argc, argv):
    if argc == 2:
        with open(argv[1], 'r') as f:
            with open("employees.tsv", 'w') as f1:
                work_files(f, f1)



if __name__ == "__main__":
    main(len(sys.argv),sys.argv)