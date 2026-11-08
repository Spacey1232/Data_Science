import sys
def caesar(text, shift):
    result = ""
    for c in text:
        if ord(c) > 127:
            raise Exception(
                "The script does not support your language yet."
            )
        if "a" <= c <= "z":
            result += chr(
                (ord(c) - ord("a") + shift) % 26 + ord("a")
            )
        elif "A" <= c <= "Z":
            result += chr(
                (ord(c) - ord("A") + shift) % 26 + ord("A")
            )
        else:
            result += c

    return result
def main(argc, argv):
    if argc != 4:
        raise Exception("Incorrect number of arguments")
    operation = argv[1]
    text = argv[2]
    shift = int(argv[3])
    if operation == "decode":
        print(caesar(text, -shift))
    elif operation == "encode":
        print(caesar(text, shift))
    else:
        raise Exception("The operation must be encode or decode")
if __name__ == "__main__":
    main(len(sys.argv), sys.argv)