import sys


def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    # Wait for user input
    c= input()
    command = c
    print(f'{command}: command not found')


if __name__ == "__main__":
    main()
