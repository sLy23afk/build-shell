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
        # if not command.strip("exit"): 
        #  continue
        
        # Check if user wants to exit
        # Print command not found error
        
        if command.lower().startswith("exit"):
            sys.exit(0 if len(command.split()) == 1 
                     else int(command.split()[1]))
        print(f"{command}: command not found")
       


if __name__ == "__main__":
    main()
