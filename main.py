import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console

from ai_config import AVAILABLE_FUNCS, MODEL_NAME, SYSTEM_PROMPT
from functions.call_function import call_function

console = Console()


def run_agent(
    client: genai.Client,
    messages: list[types.Content],
    working_directory: str,
    verbose: bool,
) -> list[types.Content]:
    for _ in range(20):
        with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT, tools=[AVAILABLE_FUNCS]
                ),
            )

            for candidate in response.candidates or []:
                if candidate.content:
                    messages.append(candidate.content)

            usage_metadata = response.usage_metadata

            if not usage_metadata:
                raise RuntimeError("Something went wrong!")

            total_tokens = usage_metadata.total_token_count
            console.print(f"[dim]Context used: {total_tokens} tokens[/dim]")

            if verbose:
                print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
                print(f"Response tokens: {usage_metadata.candidates_token_count}")

            if not response.function_calls and response.text:
                console.print(f"[bold blue]Gemini:[/bold blue] {response.text}")
                return messages

            function_responses = []
            for fc in response.function_calls or []:
                result = call_function(fc, working_directory, verbose)
                if not result or not result.parts:
                    raise Exception("fatal couldn't call a func or result has no parts")

                if verbose:
                    part = result.parts[0]
                    if part.function_response:
                        print(f"-> {part.function_response.response}")

                function_responses.append(result.parts[0])

            if function_responses:
                messages.append(types.Content(role="user", parts=function_responses))

    else:
        print("Maximum iterations reached, no final response.")
        return messages


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, nargs="?", help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--workdir",
        type=str,
        default=".",
        help="Working directory for the agent (default: current directory)",
    )
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    verbose = args.verbose
    working_directory = args.workdir
    messages = []

    if not os.path.isdir(working_directory):
        print(f"Error: Working directory '{working_directory}' does not exist.")
        return

    if args.user_prompt:
        messages.append(
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
        )
        messages = run_agent(client, messages, working_directory, verbose)

    if not args.user_prompt:
        console.print(
            "[bold yellow]Starting interactive session. Type 'exit' or 'quit' to end.[/bold yellow]"
        )

    while True:
        try:
            # If we just finished a prompt from CLI, we still drop into loop
            user_input = console.input("[bold green]User:[/bold green] ")
            if user_input.lower() in ["exit", "quit"]:
                break
            if not user_input.strip():
                continue

            messages.append(
                types.Content(role="user", parts=[types.Part(text=user_input)])
            )
            messages = run_agent(client, messages, working_directory, verbose)
        except KeyboardInterrupt, EOFError:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
