import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MODEL_NAME, SYSTEM_PROMPT


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

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )

    usage_metadata = response.usage_metadata

    if not usage_metadata:
        raise RuntimeError("Something went wrong!")

    prompt_tokens = usage_metadata.prompt_token_count
    response_tokens = usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
