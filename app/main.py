import sys
import os

def main():
    builtins = {"echo", "exit", "type"}  # List of shell builtins

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input().strip()

        if not command:
            continue

        parts = command.split()
        cmd_name = parts[0]
        cmd_args = parts[1:]

        if cmd_name == "exit":
            if len(parts) == 1:
                sys.exit(0)
            else:
                sys.exit(int(parts[1]))

        elif cmd_name == "echo":
            print(" ".join(cmd_args))

        elif cmd_name == "type":
            if len(cmd_args) < 1:
                print("Usage: type <command>")
                continue
            target = cmd_args[0]

            if target in builtins:
                print(f"{target} is a shell builtin")
            else:
                # Try to run the external program
                try:
                    # Use os.environ['PATH'] to find the executable
                    executable_path = find_executable(target)
                    if executable_path:
                        # Run the executable with arguments
                        run_external_program(executable_path, cmd_args)
                    else:
                        print(f"Error: command '{target}' not found")
                except Exception as e:
                    print(f"Error: {e}")

def find_executable(program):
    # Split the PATH environment variable into a list of directories
    path_dirs = os.environ['PATH'].split(os.pathsep)

    # Iterate over the directories and check if the program exists
    for dir in path_dirs:
        executable_path = os.path.join(dir, program)
        if os.path.exists(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path

    # If the program is not found, return None
    return None

def run_external_program(executable_path, args):
    # Use subprocess to run the executable with arguments
    import subprocess
    try:
        output = subprocess.check_output([executable_path] + args)
        print(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()