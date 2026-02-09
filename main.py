import os
from dotenv import load_dotenv
import argparse
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def main():
    print("Hello from coding-agent!")
    if api_key is None:
        raise RuntimeError("No API key found. Please set GEMINI_API_KEY in your .env file.")

    # input from user
    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument('--verbose',action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    # make API call to Gemini 2.5 flash
    client = genai.Client(api_key=api_key)

    # roles are user
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=1.0),
    )
    x = response.usage_metadata
    if x is None:
        raise RuntimeError("No usage metadata found in response. Like failed API request?")
    if args.verbose:
        print("User prompt: ", messages[0].parts[0].text)
        print("Prompt tokens: ", x.prompt_token_count)
        print("Response tokens: ", x.candidates_token_count)
        
    print("Response: ", response.text)


if __name__ == "__main__":
    main()
