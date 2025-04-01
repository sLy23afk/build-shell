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

def longest_common_prefix(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                break
    return prefix
        
def append_file(command):
    append_mode = False
    if "1>>" in command:
       command = command.replace("1>>", ">>")
    
    if ">>" not in command:
        return False
    
    parts = command.split('>>')
    if len(parts) != 2:
        return False
    cmd_part = parts[0].strip()
    output_file = parts[1].strip()
    cmd_args = shlex.split(cmd_part)   
          
    parent_dir = os.path.dirname(output_file)
    if not os.path.exists(parent_dir):
        print(f'{output_file}: No such file in the directory')
        return True
    exe_path = find_executable(cmd_args[0])
    mode = 'a' if append_mode else 'w'
    if exe_path:
        with open(output_file, 'w') as f:
            try:
                subprocess.run(cmd_args, executable=exe_path if exe_path else None, stdout=f)
            except Exception as e:
                print(f'Error: {e}')
                return True
        return True
    

def handle_error_redir(command):
    if "2>" not in command:
      return False
    
    parts = command.split("2>")
    if len(parts) != 2:
        return False
    cmd_part = parts[0].strip()
    error_file = parts[1].strip()
    cmd_args = shlex.split(cmd_part) 
    
    parent_dir = os.path.dirname(error_file)
    if not os.path.exists(parent_dir):
        print(f"{error_file}: No such file or directory")
        return True
    exe_path = find_executable(cmd_args[0])
    try:
        with open(error_file, 'w') as f:
            subprocess.run(cmd_args, executable=exe_path  if exe_path else None, stderr=f)
    except Exception as e:
            print(f"Error {e}")
            return True
    return True
    



def handle_redirection(command):            
    if "1>" in command:
       command = command.replace("1>", ">")
    
    if ">" not in command:
        return False
    
    parts = command.split('>')
    if len(parts) != 2:
        return False
    cmd_part = parts[0].strip()
    output_file = parts[1].strip()
    cmd_args = shlex.split(cmd_part)   
          
    parent_dir = os.path.dirname(output_file)
    if not os.path.exists(parent_dir):
        print(f'{output_file}: No such file in the directory')
        return True
    exe_path = find_executable(cmd_args[0])
    if exe_path:
        with open(output_file, 'w') as f:
            try:
                subprocess.run(cmd_args, executable=exe_path, stdout=f)
            except Exception as e:
                print(f'Error: {e}')
    else:
        print(f'Error: {cmd_args[0]} not found')
        return True
               
def common_name(prefix):
     matches = []
     for directory in os.environ.get("PATH", "").split(":"):
        try:
            for filename in os.listdir(directory):
                    if filename.startswith(prefix):
                        filepath = os.path.join(directory, filename)
                        if is_executable(filepath) and filename not in matches:
                            matches.append(filename)
        
        except FileNotFoundError:
          continue
     return sorted(matches)
 
    
last_completion_text = ""
tab_press_count = 0

def completer(text, state):
    global last_completion_text, tab_press_count
    
    builtin = ["echo", "exit", "type", "pwd", "cd"]
    matches = [cmd for cmd in builtin if cmd.startswith(text)]
    
    external_matches = common_name(text)
    matches.extend(external_matches)
    matches = sorted(set(matches))
    buffer = readline.get_line_buffer()
    
    if buffer == last_completion_text:
        tab_press_count += 1
    else:
        tab_press_count = 1
        last_completion_text = buffer
        matches = sorted(set(matches))
    if not matches:
         return None
    if len(matches) == 1:
        return matches[0] + ' ' if state == 0 else None
    
    lcp = longest_common_prefix(matches)
    if lcp != text and state == 0:
        return lcp  # Complete to LCP on first Tab
    elif lcp == text:
        # Tab x1 beep, Tab x2 show options
        if tab_press_count == 1 and state == 0:
            print('\a', end="", flush=True)
            return None
        elif tab_press_count == 2 and state == 0:
            print("\n" + "  ".join(matches))
            print(f"$ {buffer}", end="", flush=True)
            tab_press_count = 0
            return None
    

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    
    if buffer.startswith(last_completion_text):
        tab_press_count += 1
    else:
        tab_press_count = 1
        
    last_completion_text = buffer
    
    if tab_press_count == 1 and len(matches)> 1 and state == 0:
            print('\a', end="", flush= True)
            return None
    elif tab_press_count == 2 and len(matches) > 1 and state == 0:
            print("\n" + "  ".join(matches))
            print(f"$ {buffer}", end="", flush=True)
            tab_press_count = 0
            return None
    for directory in os.environ.get("PATH", "").split(":"):
        try:
            for filename in os.listdir(directory):
                if filename.startswith(text):
                    filepath = os.path.join(directory, filename)
                    if is_executable(filepath) and (filename + ' ') not in matches:
                        matches.append(filename + ' ')
        except FileNotFoundError:
            continue 
    
    return matches[state] + ' ' if state < len(matches) else None

 
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")


def main():
    builtins = {"echo", "exit", "pwd", "cd", "type" }
    global tab_press_count
    tab_press_count = 0
    
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()

            command = input().strip()

            if not command:
                continue
            redirection_handled = False
            
            if '2>' in command:
                if handle_error_redir(command):
                 continue
            
            if '>' in command:
                redirection_handled = handle_redirection(command)
                continue
            
            if '>' in command and not redirection_handled:
                parts = command.split('>')
                cmd_part = parts[0].strip()
                file_part = parts[1].strip()
        
    # Handle 1> (optional)
                if cmd_part.endswith('1'):
                 cmd_part = cmd_part[:-1].strip()  # remove the '1'

                 cmd_args = shlex.split(cmd_part)
                 output_file = file_part

    # Find executable
                 exe_path = find_executable(cmd_args[0])
                 if exe_path:
                     with open(output_file, 'w') as f:
                         try:
                             subprocess.run(cmd_args, executable=exe_path, stdout=f)
                         except Exception as e:
                          print(f"Error: {e}")
                 else:
                     print(f"{cmd_args[0]}: command not found")
                     continue  # Skip the rest of the loop to avoid reprocessing
            
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
