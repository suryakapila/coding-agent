import os
from google import genai
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if file_path is within working_directory
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if file exists and is a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(MAX_CHARS)
            # Check if file is larger than MAX_CHARS
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'
    

schema_get_file_content_info = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file in the working directory, truncated to a maximum number of characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)

