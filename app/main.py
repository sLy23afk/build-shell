import sys
import subprocess
import os

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def find_executable(command):
    for directory in os.environ.get("PATH", "").split(":"):
        possible_path = os.path.join(directory, command)
        if is_executable(possible_path):
            return possible_path
    return None
 
 
def main():
    builtins = {"echo", "exit", "type"}
    
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()

            command = input().strip()

            if not command:
                continue

            parts = command.split()
            cmd_name = parts[0]
            cmd_args = parts[1:]

            # Handle exit
            if cmd_name == "exit":
                sys.exit(0 if len(parts) == 1 else int(parts[1]))

            # Handle echo
            elif cmd_name == "echo":
                print(" ".join(cmd_args))

            # Handle type
            elif cmd_name == "type":
                if len(cmd_args) == 0:
                    print("Usage: type <command>")
                    continue
                target = cmd_args[0]
                if target in builtins:
                    print(f"{target} is a shell builtin")
                else:
                    exe_path = find_executable(target)
                    if exe_path:
                        print(f"{target} is {exe_path}")
                    else:
                        print(f"{target}: not found")
                continue


            # Handle external executable
            else:
             exe_path = find_executable(cmd_name)
            if exe_path:
             try:
               subprocess.run([cmd_name] + cmd_args, executable=exe_path)
             except Exception as e:
              print(f"Error executing {cmd_name}: {e}")
             else:
               continue

        except EOFError:
            break  # Handle Ctrl+D (graceful exit)
        except KeyboardInterrupt:
            print()  # Print newline after Ctrl+C and continue

if __name__ == "__main__":
    main()
