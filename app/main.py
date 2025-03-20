import sys
import subprocess
import os
import shlex
import readline

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def find_executable(command):
    for directory in os.environ.get("PATH", "").split(":"):
        possible_path = os.path.join(directory, command)
        if is_executable(possible_path):
            return possible_path
    return None
def common_name(prefix):
     matches = []
     for directory in os.environ.get("PATH", "").split(":"):
        try:
            for filename in os.listdir(directory):
                    if filename.startswith(prefix):
                        filepath = os.path.join(directory, filename)
                        if is_executable(filename) and filename not in matches:
                            matches.append(filename)
        
        except FileNotFoundError:
          continue
    
last_completion_text = ""
tab_press_count = 0

def completer(text, state):
    builtin = ["echo ", "exit ", "type ", "pwd ", "cd "]
    matches = [cmd for cmd in builtin if cmd.startswith(text)]
    external_matches = common_name(text)
    matches.append(external_matches)
    if readline.get_line_buffer().startswith(last_completion_text):
        tab_press_count += 1
    else:
        tab_press_count = 0
        
    last_completion_text = readline.get_line_buffer()
    if tab_press_count == 1 and len(matches)> 1:
            print('\a', ends=" ", flush= True)
            return None
    elif tab_press_count == 2 and len(matches) > 1:
            print(" ".join(matches))
            sys.stdout.write("$ ")
            sys.stdout.flush
            tab_press_count = 0
            return None
        
    else:
            return matches[state] + ' ' if state < len(matches) else None
    # for directory in os.environ.get("PATH", "").split(":"):
    #     try:
    #         for filename in os.listdir(directory):
    #             if filename.startswith(text):
    #                 filepath = os.path.join(directory, filename)
    #                 if is_executable(filepath) and (filename + ' ') not in matches:
    #                     matches.append(filename + ' ')
    #     except FileNotFoundError:
    #         continue 
    
    # return matches[state] if state < len(matches) else None
 
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")
def main():
    builtins = {"echo", "exit", "pwd", "cd", "type" }
    
    readline.set_completer(completer)
    readline.parse_and_bind('tab: complete')
    
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()

            command = input().strip()
            tab_press_count = 0

            if not command:
                continue
            
            parts = shlex.split(command)
            cmd_name = parts[0]
            cmd_args = parts[1:]
            
            # Handle exit
            if cmd_name == "exit":
                sys.exit(0 if len(parts) == 1 else int(parts[1]))

            # Handle echo
            elif cmd_name == "echo":
                print(" ".join(cmd_args))
                
            # Handles pwd argument
            elif cmd_name == "pwd":
                print(os.getcwd())
            
            # Handles cd 
            elif cmd_name == "cd":
                if cmd_args[0] == '~':
                    try:
                        os.chdir(os.path.expanduser('~'))
                    except Exception as e:
                        print(f"cd: {e}")       
                else:
                        try:
                            os.chdir(cmd_args[0])
                        except FileNotFoundError:
                            print(f"cd: {cmd_args[0]}: No such file or directory")
                        except Exception as e:
                            print(f"cd: {e}")
                            
                            
                        
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
                 print(f'{cmd_name}: command not found')

        except EOFError:
            break  # Handle Ctrl+D (graceful exit)
        except KeyboardInterrupt:
            print()  # Print newline after Ctrl+C and continue
     
if __name__ == "__main__":
    main()
