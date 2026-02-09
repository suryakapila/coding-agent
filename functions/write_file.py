import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if file_path is within working_directory
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # If the directory exists, return an error string
        if os.path.isdir(abs_file_path):
            return f"Error: Cannot write to '{file_path}' as it is a directory"
        dir_name = os.path.dirname(abs_file_path)
        os.makedirs(dir_name, exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'


schema_write_file_info = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)