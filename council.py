#!/home/adi/Council-Of-LLMs/.venv/bin/python

import subprocess
import re
from rich.console import Console
from rich.panel import Panel

console = Console()

MAX_ROUNDS = 2

AGENTS = [
    {
        "name": "BJP Andhbhakt",
        "model": "ministral-3:14b",
        "style": "defends modi under any cost, patriotic, emotional, nationalist, will defend any action by bjp,"
        "cares about hindutva, cow protection, religious values, casteism",
        "color": "yellow",
    },
    {
        "name": "Far Left Self-Proclaimed Intellectual Indian",
        "model": "ministral-3:14b",
        "style": "democratic social, pro-minorities, secular, supports free speech, critical of government, cares about social justice, equality, human rights, progressive",
        "color": "green",
    },
    {
        "name": "Educated Historian",
        "model": "qwen3-coder:latest",
        "style": "neutral, balanced, pragmatic, focuses on facts and data, avoids extreme views, considers multiple perspectives, "
        "holds multiple degrees in history and political science",
        "color": "cyan",
    },
    
]

PROMPT_TEMPLATE = """
You are acting as: {role}.
Your thinking style: {style}.

TASK:
{question}

RULES:
- Be independent and critical.
- Do NOT agree with others by default.
- Be concise but precise.
- Generate as fast as possible.

OUTPUT FORMAT (STRICT):
FINAL_ANSWER:
<your answer>

VOTE:
<number from 1 to 10>

CRITIQUE:
<1-3 sentences>

1 LINE SUMMARY:
<your summary>
"""

def run_agent(agent, question):
    prompt = PROMPT_TEMPLATE.format(
        role=agent["name"],
        style=agent["style"],
        question=question,
    )

    proc = subprocess.Popen(
        ["ollama", "run", agent["model"]],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )

    proc.stdin.write(prompt)
    proc.stdin.close()

    full_output = ""

    console.print(f"[italic {agent['color']}]Generating…[/]\n", end="")

    for line in proc.stdout:
        full_output += line
        console.print(line, end="", style=agent["color"])

    proc.wait()

    vote_match = re.search(r"VOTE:\s*(\d+)", full_output)
    vote = int(vote_match.group(1)) if vote_match else 0

    return full_output.strip(), vote

def run_council(question):
    agents = AGENTS.copy()
    round_num = 1

    while len(agents) > 1 and round_num <= MAX_ROUNDS:
        console.rule(f"[bold]ROUND {round_num}[/bold]")

        results = []

        for agent in agents:
            console.rule(f"[{agent['color']}]{agent['name']}[/]")
            output, vote = run_agent(agent, question)

            console.print(
                Panel(
                    output,
                    title=f"{agent['name']} (Vote: {vote})",
                    border_style=agent["color"],
                )
            )

            results.append((agent, vote))

        results.sort(key=lambda x: x[1])
        eliminated = results[0][0]

        console.print(
            f"\n[bold red]ELIMINATED:[/] {eliminated['name']} "
            f"(model: {eliminated['model']})\n"
        )

        agents = [a for a, _ in results[1:]]
        round_num += 1

    console.rule("[bold green]FINAL WINNER[/bold green]")
    console.print(f"[bold]{agents[0]['name']}[/]")

def main():
    console.print(
        "[bold green]Council of LLMs[/bold green] "
        "(type 'exit' or 'quit' to leave)\n"
    )

    while True:
        try:
            question = console.input("[bold]Enter your question:[/] ").strip()
        except EOFError:
            console.print("\n[italic]Goodbye.[/italic]")
            break

        if question.lower() in {"exit", "quit"}:
            console.print("[italic]Goodbye.[/italic]")
            break

        if not question:
            continue

        run_council(question)

        console.print("\n[dim]Ask another question or type 'exit'.[/dim]\n")

if __name__ == "__main__":
    main()
