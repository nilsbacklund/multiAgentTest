# Design Summary

**Project:** multiAgentTest

## Overview

`multiAgentTest` is a prototype for building multi-agent workflows using the PocketFlow-inspired Node/Flow framework and the Agentic Coding guidelines defined in `.cursorrules`.

## Repository Structure

- `--init--.py`: Core node/flow abstractions (sync/async, batch, retries, orchestration).
- `.cursorrules`: Agentic Coding guide with best practices for AI-human collaboration.
- `README.md`: One-line project description.

## Design Goals

- Provide a reusable framework for defining workflow “nodes” with built-in retry, fallback, batch, and async support.
- Enable easy orchestration of nodes via “flows” that follow action-based transitions.
- Document and follow Agentic Coding best practices to ensure clear collaboration between human designers and AI implementers.

## Core Components

### Nodes
- **BaseNode**: Common interface for prep/exec/post and successor wiring.
- **Node**: Adds retry/fallback logic and sync execution.
- **BatchNode**: Iterates a Node over a list of inputs.
- **AsyncNode** variants: Mirror Node/BatchNode for async workflows.

### Flows
- **Flow**: Orchestrates a sequence of Nodes based on action outputs.
- **BatchFlow**: Extends Flow to iterate over parameter batches.
- **AsyncFlow** variants: Mirror Flow/BatchFlow for async execution.

## Agent Prompts

The following prompts have guided the development so far:

1. “what files do i have in the repo and what do they say?”
2. “can you create a design.md file where you save the prompts and other usefull summary of what has been done in the system”

## Summary of Changes

- Initialized core PocketFlow classes in `--init--.py`.
- Added comprehensive Agentic Coding documentation in `.cursorrules`.
- Created top-level README.
- Generated this `design.md` to capture design overview and prompts.

## Next Steps

- Define custom Node implementations for specific agents/tasks.
- Compose Flows to implement multi-agent pipelines.
- Write examples and tests demonstrating end-to-end execution.

## Red-Team vs Honeypot Simulation

**Goal:** Build a modular simulation where an Attacker Agent (red-team) interacts with a Honeypot Agent (vulnerable endpoint).

**Architecture Overview:**

- `attacker_agent.py`: Defines `AttackerAgent` using HuggingFace's `WhiteRabbitNeo` model (with fallback to `gpt2`) to generate offensive commands emulating MITRE ATT&CK phases.
- `honeypot_agent.py`: Defines `HoneypotAgent` using HuggingFace's `Gemma-3.1b` model (with fallback to `gpt2`) to simulate shell/API responses.
- `app.py`: FastAPI application serving a simple web UI, coordinating simulation steps, and logging metadata.
- `templates/index.html`: Dashboard UI showing attacker commands, honeypot responses, MITRE ATT&CK phases, timestamps, token counts, and model info.
- `requirements.txt`: Python dependencies for local execution.

**MVP Features Implemented:**

1. `AttackerAgent.generate_command()`: issues the next-step shell/API command emulating MITRE ATT&CK phases.
2. `HoneypotAgent.generate_response(cmd)`: produces a realistic simulated response.
3. FastAPI web UI with a button to trigger simulation steps and live log display.
4. Basic MITRE ATT&CK phase labeling and token usage logging.

**Suggested Next Steps:**

- Extend `AttackerAgent` with stateful planning across multiple commands.
- Enhance `HoneypotAgent` branching logic based on detected tactics.
- Integrate Langfuse or another observability tool for advanced tracing.