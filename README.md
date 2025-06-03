# multiAgentTest
Test to create a multi agent system using pocketflow and cursorrules

## Red-Team vs Honeypot Simulation

This project includes a minimal web-based red-team vs honeypot simulation:

- `attacker_agent.py`: Generates attacker commands using WhiteRabbitNeo.
- `honeypot_agent.py`: Simulates vulnerable responses using Gemma-3.1b.
- `app.py`: FastAPI app serving a dashboard to run simulation steps.
- `templates/index.html`: Dashboard UI.

### Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

*Note:* If the specified models (`WhiteRabbitNeo` or `Gemma-3.1b`) are not found locally, the agents will fall back to `gpt2`.

### Run the dashboard

```bash
uvicorn app:app --reload
```

Open http://127.0.0.1:8000 in your browser.
