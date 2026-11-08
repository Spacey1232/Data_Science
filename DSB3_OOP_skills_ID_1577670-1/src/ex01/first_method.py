def main():
    class Research():
        def file_reader(self):
            with open("data.csv") as f:
                return f.read()
    reader = Research()
    print(reader.file_reader(), end="")
if __name__ == "__main__":
    main()