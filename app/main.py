import sys
import subprocess
import os

def is_executable(path):
    # Check if a file exists and is executable.
    return os.path.isfile(path) and os.access(path, os.X_OK)

def find_executable(command):
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
        cmd_name = parts[0]
        cmd_args = parts[1:]

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
            target1 = cmd_args[0]

            # Check if it's a builtin
            if cmd_name in builtins:
                print(f"{cmd_name} is a shell builtin")
            else:
                exe_path = find_executable(target1)
                if exe_path:
                    print(f'{target1} is {exe_path}]')
                else:
                    print(f'{target1}: not found')
                continue
            
            # Search in PATH
            exe_path = find_executable(cmd_name)
            if exe_path:
                try:
                    subprocess.run([cmd_name] + target1)
                except Exception as e:
                    print(f"Error executing {cmd_name}: {e}")
            else:
                print(f'{cmd_name}: not found')
        
        # If command is unknown
            
            # Find and run the command.exe
            # exe_path = find_executable(cmd_name)
            # if exe_path:
            #     try:
            #         subprocess.run([exe_path] + cmd_args)
            #     except Exception as e:
            #      print(f"Error executing {cmd_name}: {e}")
            # else:
            #  print(f"{cmd_name}: command not found")
    
if __name__ == "__main__":
    main()
