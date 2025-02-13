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
        word_check = "echo"
        command = input()
        parts = command.split()
        
        # Check if input is empty (user pressed Enter)
        # if not command.strip("exit"): 
        #  continue
        
        # Check if user wants to exit
        # Print command not found error
        #to check the echo command
        # if command == "echo" and len(command.split()) > 1:
        # print(command.split(0, 1))
        while parts[0] == "echo":
         if len(parts) > 1:
          parts = ' '.join(parts[1:]) 
          print (parts) 
        # else: 
        #     # parts[0:] == 'echo':   
         if word_check not in command:
        # next = input()
          print(f"{next}: command not found") 
         elif command.lower().startswith("exit"):
            sys.exit(0 if len(next.split()) == 1 
                     else int(next.split()[1]))
            
       


if __name__ == "__main__":
    main()
