import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ai_config import AVAILABLE_FUNCS, MODEL_NAME, SYSTEM_PROMPT
from functions.call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    user_prompt = args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT, tools=[AVAILABLE_FUNCS]
            ),
        )

        if not response.function_calls and response.text:
            print("Final response:")
            print(response.text)
            break

        for candidate in response.candidates or []:
            if candidate.content:
                messages.append(candidate.content)

        usage_metadata = response.usage_metadata

        if not usage_metadata:
            raise RuntimeError("Something went wrong!")

        prompt_tokens = usage_metadata.prompt_token_count
        response_tokens = usage_metadata.candidates_token_count

        if args.verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        function_responses = []
        for fc in response.function_calls or []:
            result = call_function(fc, args.verbose)
            if not result:
                raise Exception("fatal couldn't call a func")
            elif args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])

        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))

    else:
        print("Maximum iterations reached, no final response.")


if __name__ == "__main__":
    main()
