from google.genai import types

from ai_config import FUNCS_TO_CALL


def call_function(
    function_call: types.FunctionCall, working_directory: str, verbose: bool = False
) -> types.Content:
    fc_name = function_call.name or "unknown_function"
    fc_args = function_call.args or {}

    if verbose:
        print(f"Calling function: {fc_name}({fc_args})")
    else:
        print(f" - Calling function: {fc_name}")

    fc_args["working_directory"] = working_directory

    func = FUNCS_TO_CALL.get(fc_name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fc_name,
                    response={"error": f"Unknown function: {fc_name}"},
                )
            ],
        )

    try:
        result = func(**fc_args)
    except Exception as e:
        result = f"Error executing function: {e}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fc_name,
                response={"result": result},
            )
        ],
    )
