#!/usr/bin/env python3

import subprocess
import re
from rich.console import Console
from rich.panel import Panel

console = Console()

AGENTS = [
    # --- Ministral agents ---
    {
        "name": "Indie Dev",
        "model": "ministral-3:14b",
        "style": "shipping mindset, simple and practical",
        "color": "green",
    },
    {
        "name": "Optimizer",
        "model": "ministral-3:14b",
        "style": "reduces complexity, refactors aggressively",
        "color": "blue",
    },
    {
        "name": "Skeptic",
        "model": "ministral-3:14b",
        "style": "finds flaws, distrusts assumptions",
        "color": "red",
    },
    {
        "name": "Career Advisor",
        "model": "ministral-3:14b",
        "style": "long-term consequences, realism",
        "color": "yellow",
    },
    {
        "name": "Pragmatist",
        "model": "ministral-3:14b",
        "style": "what works now, minimal theory",
        "color": "cyan",
    },
    {
        "name": "Wildcard",
        "model": "ministral-3:14b",
        "style": "creative, unconventional, risky ideas",
        "color": "bright_black",
    },

    # --- Qwen heavy hitters ---
    {
        "name": "Senior Architect",
        "model": "qwen3-coder:30b",
        "style": "system design, scalability, long-term maintenance",
        "color": "magenta",
    },
    {
        "name": "Systems Reviewer",
        "model": "qwen3-coder:30b",
        "style": "deep critique, edge cases, failure modes",
        "color": "white",
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

OUTPUT FORMAT (STRICT):
FINAL_ANSWER:
<your answer>

VOTE:
<number from 1 to 10>

CRITIQUE:
<1-3 sentences>
"""

def run_agent(agent, question):
    prompt = PROMPT_TEMPLATE.format(
        role=agent["name"],
        style=agent["style"],
        question=question,
    )

    proc = subprocess.run(
        ["ollama", "run", agent["model"]],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    output = proc.stdout.decode()

    vote_match = re.search(r"VOTE:\s*(\d+)", output)
    vote = int(vote_match.group(1)) if vote_match else 0

    return output.strip(), vote

def main():
    question = console.input("[bold]Enter your question:[/] ")

    agents = AGENTS.copy()
    round_num = 1

    while len(agents) > 1:
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

if __name__ == "__main__":
    main()
#!/usr/bin/env python3