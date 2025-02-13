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
        case = "type"
        word_check = "echo"
        case1 = "exit"
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
        if parts[0] == case: 
            if parts[-1] == word_check:
              print(f"{parts[-1]} is a shell builtin")
            elif parts[-1] == case1:
                print(f"{parts[-1]} is a shell builtin")
            else:
                continue
        if command.lower().startswith("exit"):
            sys.exit(0 if len(command.split()) == 1 
                         else int(command.split()[1]))
        elif parts[0] == "echo":
            if len(parts) > 1:
             parts = ' '.join(parts[1:]) 
             print (parts) 
        # else: 
        #     # parts[0:] == 'echo':   
        elif word_check not in parts:
        # next = input()
          print(f"{command}: command not found") 
        
            
       


if __name__ == "__main__":
    main()
