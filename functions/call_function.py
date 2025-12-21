from google.genai import types

from ai_config import FUNCS_TO_CALL


def call_function(function_call: types.FunctionCall, verbose=False) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_call.args["working_directory"] = "calculator"

    args = function_call.args
    func = FUNCS_TO_CALL.get(function_call.name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )

    args = function_call.args
    result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": result},
            )
        ],
    )
