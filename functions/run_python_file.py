import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        #check if file_path is within working_directory
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        #check if file exists and is a regular file using os.path.isfile, if nor return an error string
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        #check if file has .py extension, if not return an error string
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        #construct the command to run the python file with arguments
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        
        #run the subprocess and capture the output and errors, set a timeout of 30 seconds , workng directory, capture output , decode the output to string
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=abs_working_dir)
        output = []
        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        if not result.stdout and not result.stderr:
            output.append('No output was produced')
        if result.stdout and not result.stderr:
            output.append(f'STDOUT:{result.stdout.strip()}')
        if result.stderr and not result.stdout:
            output.append(f'STDERR:{result.stderr.strip()}')
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
        
