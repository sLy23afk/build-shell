import sys
import subprocess
import os

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
        cmd_name = parts[0]
        cmd_args = parts[1:]

        # Handle `exit`
        if cmd_name == "exit":
            sys.exit(0 if len(parts) == 1 else int(parts[1]))

        # Handle `echo` (print everything after "echo")
        elif cmd_name == "echo":
            print(" ".join(cmd_args))
        
        # Handle `type` command
        elif cmd_name == "type":
            if len(cmd_args) < 1:
                print("Usage: type <command>")
                continue
            target = cmd_args[0]

            # Check if it's a builtin
            if target in builtins:
                print(f"{target} is a shell builtin")
            else:
                exe_path = find_executable(target)
                if exe_path:
                    print(f'{target} is {exe_path}')
                else:
                    print(f'{target}: not found')
            continue  # Skip to the next prompt
        
        # Check if it's an external executable
        exe_path = find_executable(cmd_name)
        if exe_path:
            try:
                # Run the external command with arguments
                subprocess.run([exe_path] + cmd_args, executable = exe_path, text=True)
            except Exception as e:
                print(f"Error executing {cmd_name}: {e}")
        else:
            print(f"{cmd_name}: command not found")

if __name__ == "__main__":
    main()
