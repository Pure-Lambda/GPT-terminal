#!/usr/bin/env python3

from openai import OpenAI
import os
import sys

# check that OPENAI_API_KEY is defined:
if not os.environ.get("OPENAI_API_KEY"):
    raise Exception("OPENAI_API_KEY is not defined")

# check that SCRIPT is defined:
if not os.environ.get("SCRIPT"):
    raise Exception("SCRIPT is not defined")

def get_completion(log_history, prompt, model="gpt-3.5-turbo"):
    openai = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    messages = [
        {"role": "system", "content": """
As an expert in CLI, dev, bash and all dev related fields, you can review terminal logs, provide insights and suggest commands if needed.
You will review the previous script log context, before answering.

You will then answer the user in two possible ways, either with one simple command to achieve the desire outcome or information on what is happening.
When the answer is one single command, only return the command with no explanation. If needed, the user will ask for more information.
        """},
        {
            "role":"system",
            "content": f"""
Current date is {os.popen("date").read()}

This is the log history:
```
{log_history}
```
        """},
        {"role": "user", "content": prompt}
        ]

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content

def get_log_history():
    # get the last 1000 non-blank lines from the file located at the path described by the env: FILE_SCRIPT_LOG
    return os.popen("grep -v '^$' " + os.environ.get("SCRIPT") + " | tail -n 20").read()


# Main:
if __name__ == "__main__":
    log_history = get_log_history()
    prompt = " ".join(sys.argv[1:])
    print(get_completion(log_history, prompt))
