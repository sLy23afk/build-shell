import sys


def main():
 while True   # Uncomment this block to pass the first stage
  sys.stdout.write("$ ")

    # Wait for user input
    



    # Print the prompt
command = input("$")
    
    # Check if input is empty (user pressed Enter)
if not command.strip():
        continue
    
    # Print command not found error
print(f"{command}: command not found")


if __name__ == "__main__":
    main()
