from app.services.ai_service import ask_ai
import json
from app.services.tools import get_weather, calculate

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
    {TOOLS}

    User question:
    {question}

    If a tool is needed, respond ONLY in JSON format like:

    {{
    "tool": "tool_name",
    "arguments": {{
        "param": "value"
    }}
    }}

    If no tool needed:
    {{
    "tool": null
    }}
    
    """
    decision = ask_ai(prompt)
    decision_data = json.loads(decision)

    tool_name = decision_data["tool"]

    if tool_name:
        arguments = decision_data["arguments"]

        tool_function = TOOL_MAP[tool_name]

        result = tool_function(**arguments)
    final_prompt = f"""
    User question:
    {question}

    Tool used:
    {tool_name}

    Tool result:
    {result}

    Generate final helpful response.
    """
    final_answer = ask_ai(final_prompt)

    return final_answer