# import sys


# def main():
#     sys.stdout.write("$ ")

# command = input()    
# while True:
#  print(f"{command}: command not found")


#  if __name__ == "__main__":
#     main(command)

import sys
import subprocess
import os
# path = PATH="/usr/bin:/usr/local/bin"

# def executepth(path):
#  return os.path.isfile(path) and os.access(path, os.X_OK)
# def findexe(command):
#  for directory in os.environ.get("PATH", " ").split(":"):
#      possiblepath = os.path.join(directory, command)
#      if executepth(possiblepath):
#          return possiblepath
#      return None

# def main():
#     while True:
#         sys.stdout.write("$ ")
#         sys.stdout.flush()
#         case = "type" 
#         word_check = "echo" 
#         case1 = "exit"
#         command = input()
#         parts = command.split()
#         # Check if input is empty 
#         # if not command.strip("exit"): 
#         #  continue

#         if parts[0] == case: 
#             if parts[-1] == word_check:
#               print(f"{parts[-1]} is a shell builtin")
#             elif parts[-1] == case1:
#                 print(f"{parts[-1]} is a shell builtin")
#             elif parts[-1] == case:
#                 print(f'{parts[-1]} is a shell builtin')    
#             else:
#                 print(f'{parts[-1]}: not found')
#         if command.lower().startswith("exit"):
#             sys.exit(0 if len(command.split()) == 1 
#                          else int(command.split()[1]))
#         elif parts[0] == "echo":
#             if len(parts) > 1:
#              parts = ' '.join(parts[1:]) 
#              print (parts)  
#         elif word_check not in parts and case not in parts:
#           print(f"{command}: command not found") 
#           continue
#         cmd_name = parts[1]
#         executable_path = findexe(cmd_name)
#         if executable_path:
#                 print(f"{cmd_name} is {executable_path}")
#         else:
#                 print(f"{cmd_name}: not found")         
       
# if __name__ == "__main__":
#     main()
#!/usr/bin/env python3
def is_executable(path):
    """Check if a file exists and is executable."""
    return os.path.isfile(path) and os.access(path, os.X_OK)

def find_executable(command):
    """Search for an executable in the PATH directories."""
    for directory in os.environ.get("PATH", "").split(":"):
        possible_path = os.path.join(directory, command)
        if is_executable(possible_path):
            return possible_path
    return None

def main():
    builtins = {"echo", "exit", "type"}  # List of shell builtins
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input().strip()
        
        # If user just presses enter, show the prompt again
        if not command:
            continue

        parts = command.split()

        # Handle `exit`
        if parts[0] == "exit":
            sys.exit(0 if len(parts) == 1 else int(parts[1]))

        # Handle `echo` (print everything after "echo")
        elif parts[0] == "echo":
            print(" ".join(parts[1:]))
        
        # Handle `type` command
        elif parts[0] == "type":
            if len(parts) < 2:
                print("Usage: type <command>")
                continue

            cmd_name = parts[1]

            # Check if it's a builtin
            if cmd_name in builtins:
                print(f"{cmd_name} is a shell builtin")
                continue

            # Search in PATH
            executable_path = find_executable(cmd_name)
            if executable_path:
                print(f"{cmd_name} is {executable_path}") 
            else:
                print(f"{cmd_name}: not found")
        
        # If command is unknown
        else:
            print(f"{command}: command not found")
            
            # Find and run the command.exe
            exe_path = find_executable(cmd_name)
            if exe_path:
                try:
                    subprocess.run([exe_path] + cmd_args)
                except Exception as e:
                print(f"Error executing {cmd_name}: {e}")
            else:
             print(f"{cmd_name}: command not found")
    
if __name__ == "__main__":
    main()
