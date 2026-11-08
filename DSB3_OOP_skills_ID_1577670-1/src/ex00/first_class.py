def main():
    class Must_Read():
        with open("data.csv") as f:
            for line in f:
                print(line, end="")
if __name__ == "__main__":
    main()