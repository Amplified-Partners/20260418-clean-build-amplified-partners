#!/usr/bin/env python3
"""
Grok Agent — xAI Grok API via OpenAI SDK
Interactive loop with shell tool capability.
"""

import json
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
XAI_API_KEY = os.getenv("XAI_API_KEY")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

MODEL = "grok-3"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "shell",
            "description": "Run a shell command and return stdout/stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {
                        "type": "string",
                        "description": "The shell command to execute.",
                    }
                },
                "required": ["cmd"],
            },
        },
    }
]


def run_shell(cmd: str) -> str:
    """Execute a shell command and return combined output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
    )
    output = result.stdout
    if result.stderr:
        output += f"\nSTDERR:\n{result.stderr}"
    if result.returncode != 0:
        output += f"\nEXIT CODE: {result.returncode}"
    return output.strip() or "(no output)"


def process_tool_call(tool_call) -> str:
    """Dispatch a tool call and return the result as a string."""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if name == "shell":
        cmd = args["cmd"]
        print(f"\n[shell] $ {cmd}")
        result = run_shell(cmd)
        print(f"[shell] {result}")
        return result

    return f"Unknown tool: {name}"


def run_agent(user_message: str, history: list) -> list:
    """
    Run one agent turn: user message -> completions loop until no tool calls.
    Returns updated history.
    """
    history.append({"role": "user", "content": user_message})

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # Append assistant message to history
        history.append(message.model_dump(exclude_unset=False))

        # If no tool calls, we're done
        if not message.tool_calls:
            print(f"\nGrok: {message.content}")
            break

        # Process each tool call and append results
        for tool_call in message.tool_calls:
            result = process_tool_call(tool_call)
            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    return history


def main():
    print("Grok Agent — type 'exit' or 'quit' to stop.\n")

    system_message = {
        "role": "system",
        "content": (
            "You are a helpful AI agent with access to a shell tool. "
            "Use it when the user asks you to run commands, check files, "
            "or interact with the system. Be direct and concise."
        ),
    }

    history = [system_message]

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Exiting.")
            break

        history = run_agent(user_input, history)


if __name__ == "__main__":
    main()
