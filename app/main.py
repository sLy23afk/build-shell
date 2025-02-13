# import sys


# def main():
#     sys.stdout.write("$ ")

# command = input()    
# while True:
#  print(f"{command}: command not found")


#  if __name__ == "__main__":
#     main(command)

import sys
import os
path = PATH="/usr/bin:/usr/local/bin"

def executepth(path):
 return os.path.isfile(path) and os.access(path, os.X_OK)
def findexe(command):
 for directory in os.environ.get("PATH", " ").split(":"):
     possiblepath = os.path.join(directory, command)
     if executepth(possiblepath):
         return possiblepath
     return None

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        case = "type" 
        word_check = "echo" 
        case1 = "exit"
        command = input()
        parts = command.split()
        # Check if input is empty 
        # if not command.strip("exit"): 
        #  continue

        if parts[0] == case: 
            if parts[-1] == word_check:
              print(f"{parts[-1]} is a shell builtin")
            elif parts[-1] == case1:
                print(f"{parts[-1]} is a shell builtin")
            elif parts[-1] == case:
                print(f'{parts[-1]} is a shell builtin')    
            else:
                print(f'{parts[-1]}: not found')
        if command.lower().startswith("exit"):
            sys.exit(0 if len(command.split()) == 1 
                         else int(command.split()[1]))
        elif parts[0] == "echo":
            if len(parts) > 1:
             parts = ' '.join(parts[1:]) 
             print (parts)  
        elif word_check not in parts and case not in parts:
          print(f"{command}: command not found") 
          continue
        cmd_name = parts[1]
        executable_path = findexe(cmd_name)
        if executable_path:
                print(f"{cmd_name} is {executable_path}")
        else:
                print(f"{cmd_name}: not found")         
       


if __name__ == "__main__":
    main()
