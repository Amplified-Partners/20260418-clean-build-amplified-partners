#!/usr/bin/env python3
import ollama

COUNCIL = {
    "strategist": "llama3.1",
    "analyst": "qwen3:8b", 
    "executor": "llama3.2"
}

# EDIT THIS - your message to the council
MY_MESSAGE = """
I want to apply the pudding technique to help a small business.
The technique: chunk data, label it, score with a rubric, mix chunks,
look for symbiotic outcomes where 1+1=3.

How do I start? What should my first rubric be?
"""

print("=" * 60)
print("COUNCIL CHAT - Your Message:")
print("=" * 60)
print(MY_MESSAGE)

for role, model in COUNCIL.items():
    print(f"\n{'='*60}")
    print(f"🎙️ {role.upper()} ({model}) responds:")
    print("=" * 60)
    response = ollama.generate(
        model=model,
        prompt=f"Ewan asks: {MY_MESSAGE}\n\nAs the {role}, give your best advice. Be brief, actionable.",
        options={"temperature": 0.8}
    )
    print(response["response"])
