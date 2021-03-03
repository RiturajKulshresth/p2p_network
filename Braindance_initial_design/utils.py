import os

cwd = os.getcwd()
path_to_file = cwd + "/read_file.txt"
new_file_path = cwd + "/new_file.txt"


def convertToBytes(file_path=path_to_file):
    read_data = None
    with open(file_path, 'r') as file:
        read_data = file.read()
    return read_data.encode("utf-8")


def createFile(data):
    data = data.decode("utf-8")
    print("Writing to file")
    with open(new_file_path, 'a') as file:
        file.write(data)
    return True


def main():
    data = convertToBytes()
    print("Data: ", data)
    createFile(data)


if __name__ == "__main__":
    main()
