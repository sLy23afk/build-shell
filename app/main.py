# import sys


# def main():
#     sys.stdout.write("$ ")

# command = input()    
# while True:
#  print(f"{command}: command not found")


#  if __name__ == "__main__":
#     main(command)

import sys

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        
        # Check if input is empty (user pressed Enter)
        if not command.exit(): 
         continue
        
        
        # Print command not found error
        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
