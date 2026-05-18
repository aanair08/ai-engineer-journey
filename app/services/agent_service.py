from app.services.ai_service import ask_ai
import json
from app.services.tools import get_weather, calculate
import json
from app.schemas.tools_schema import ToolDecision

TOOLS = [
    {
        "name": "get_weather",
        "description": "Get weather information for a city",
        "parameters": {
            "city": "string"
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculation",
        "parameters": {
            "expression": "string"
        }
    }
]


TOOL_MAP = {
    "get_weather": get_weather,
    "calculate": calculate
}

def detect_tool(question):
    q = question.lower()

    if "weather" in q:
        return "weather"

    if "calculate" in q or "+" in q or "-" in q:
        return "calculate"

    return None


def run_agent(question):
    prompt = f"""
    You are an AI agent.

    Available tools:
    - get_weather
    - calculate

    Respond ONLY with valid JSON.

    Valid format:
    {{
    "tool": "get_weather",
    "arguments": {{
        "city": "Kerala"
    }}
    }}

    OR

    {{
    "tool": null,
    "arguments": {{}}
    }}

    User question:
    {question}
    """
    decision = ask_ai(prompt)

    print("\n=== RAW LLM DECISION ===")
    print(decision)

    # -----------------------------
    # Step 2: Parse + Validate JSON
    # -----------------------------

    try:
        parsed_json = json.loads(decision)

        decision_data = ToolDecision(**parsed_json)

    except Exception as e:
        return f"Invalid AI response: {str(e)}"


    tool_name = decision_data.tool
    arguments = decision_data.arguments

    print("\n=== VALIDATED DECISION ===")
    print("Tool:", tool_name)
    print("Arguments:", arguments)


    if tool_name is None:
        return ask_ai(question)



    if tool_name not in TOOL_MAP:
        return f"Unknown tool: {tool_name}"


    try:
        tool_function = TOOL_MAP[tool_name]

        tool_result = tool_function(**arguments)

    except Exception as e:
        return f"Tool execution failed: {str(e)}"

    print("\n=== TOOL RESULT ===")
    print(tool_result)


    final_prompt = f"""
    User question:
    {question}

    Tool used:
    {tool_name}

    Tool result:
    {tool_result}

    Generate a helpful final response for the user.
    """

    final_answer = ask_ai(final_prompt)

    return final_answer