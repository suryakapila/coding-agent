import os
from dotenv import load_dotenv
import argparse
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]
    for _ in range(20):
        # call the model, handle responses, etc.
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
                
        x = response.usage_metadata
        if x is None:
            raise RuntimeError("No usage metadata found in response. Like failed API request?")
        if args.verbose:
            print("User prompt: ", messages[0].parts[0].text)
            print("Prompt tokens: ", x.prompt_token_count)
            print("Response tokens: ", x.candidates_token_count)
        candidate = response.candidates[0]
        function_responses = []
        function_calls_found = False
        
        for part in candidate.content.parts:
            if part.function_call is not None:
                function_calls_found = True
                function_call_result = call_function(part.function_call, verbose=args.verbose)
                # 1
                if not function_call_result.parts:
                    raise Exception("Expected function_call_result.parts to be non-empty.")
                tool_part = function_call_result.parts[0]
                # 2
                if tool_part.function_response is None:
                    raise Exception("Expected part.function_response to be non-None.")
                #3
                if tool_part.function_response.response is None:
                    raise Exception("Expected part.function_response.response to be non-None.") 

                function_result = tool_part.function_response.response["result"]

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(tool_part)

        if function_calls_found:
                messages.append(types.Content(
                    role="user",
                    parts=function_responses
                ))
        else:
            print("Final Response: ")        
            print(response.text)
            return 
        
    print("Max iterations reached, exiting.")
    sys.exit(1)
    


if __name__ == "__main__":
    main()
