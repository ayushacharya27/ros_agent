# ROS Agent v2

ROS Agent v2 is a multi-agent framework for autonomous ROS 2 development. It leverages LLMs to understand user requirements, inspect existing workspaces, retrieve official ROS 2 documentation, generate execution plans, and build ROS 2 projects through structured tool use.

---

## Features

- Multi-agent workflow using LangGraph
- Workspace-aware planning and execution
- ROS 2 documentation retrieval
- Autonomous ROS 2 package generation
- Terminal command generation and execution
- Modular tool architecture
- Extensible agent pipeline
- Incremental workspace verification
- Persistent AgentState support (PostgreSQL - WIP)

---

## Architecture

```text
                User Goal
                    │
                    ▼
            Planner Agent
                    │
          High-Level Plan
                    │
                    ▼
            Builder Agent
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 Workspace      ROS2 Docs     Web Search
  Reader         Scraper
      └─────────────┼─────────────┘
                    ▼
        Command Generation
                    │
                    ▼
         Terminal Execution
                    │
                    ▼
        Updated ROS2 Workspace
```

---

## Project Structure

```text
ros_agentv2/
├── Agents/
├── AgentState/
├── workflow/
├── tools/
├── database/
├── test_agent.py
└── README.md
```

---

## Agents

### Planner
- Converts user goals into structured implementation plans.
- Determines package structure and execution sequence.

### Builder
- Reads the current workspace.
- Retrieves official ROS 2 documentation.
- Identifies missing components.
- Generates executable terminal commands.
- Executes and verifies each step.

---

## Tools

| Tool | Purpose |
|------|---------|
| Workspace Reader | Reads and summarizes the ROS 2 workspace |
| Terminal Tool | Executes shell commands |
| Web Search | Finds relevant ROS 2 documentation |
| Web Scraper | Extracts implementation details from official documentation |

---

## Technology Stack

- Python
- ROS 2
- LangGraph
- LangChain
- Mistral AI
- Firecrawl
- PostgreSQL
- SQLAlchemy
- python-dotenv

---

## Installation

```bash
git clone https://github.com/<username>/ros_agentv2.git
cd ros_agentv2

python -m venv ros_agentv2
source ros_agentv2/bin/activate

pip install -r requirements.txt
```

Create a `.env`

```env
MISTRAL_API_KEY=your_api_key
FIRECRAWL_API_KEY=your_api_key
```

---

## Usage

```bash
python test_agent.py
```

---

# Development Log

## 22 May 2026 — PostgreSQL Integration

### Goal

Introduce persistent storage for `AgentState` so workflows can recover from failures and resume execution.

### PostgreSQL Setup

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib

sudo systemctl start postgresql
sudo systemctl status postgresql
```

Create a database and user:

```sql
CREATE DATABASE <database_name>;

CREATE USER <user_name> WITH PASSWORD '<password>';

GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <user_name>;
ALTER SCHEMA public OWNER TO <user_name>;
```

Database module layout:

```text
database/
├── __init__.py
├── database.py        # PostgreSQL connection
├── models.py          # SQLAlchemy models
└── create_tables.py   # Creates database tables
```

Create tables:

```bash
python3 -m database.create_tables
```

At this stage, PostgreSQL is configured but not yet integrated into the agent workflow.

---

## Initial Agent Development

Implemented:

- Planner Agent
- Terminal execution tool
- Workspace reader
- Documentation search and scraping tools

Running package modules:

```bash
python3 -m <package_name>.<module_name>
```

---

## Planned Architecture Changes

The architecture is evolving toward a supervisor-based multi-agent system.

A **Reasoner Agent** will act as the central coordinator, dynamically deciding which specialized agent should execute next.

Planned architecture:

```text
                    User Goal
                        │
                        ▼
                Reasoner Agent
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    Planner        Builder         GitHub Agent
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                 Verification Agent
                        │
                        ▼
                Updated AgentState
```

Responsibilities of the Reasoner Agent:

- Interpret user intent
- Delegate tasks to specialized agents
- Maintain execution flow
- Handle failures and retries
- Decide when to re-plan
- Coordinate long-running workflows
- Support iterative development loops

---

## Roadmap

- Reasoner Agent
- Code Generation Agent
- Verification Agent
- Debugging Agent
- GitHub Agent
- Persistent AgentState integration
- Memory-enabled workflows
- Autonomous iterative development
- Runtime debugging
- CI/CD integration

---

## Vision

ROS Agent v2 aims to evolve into an autonomous ROS software engineering system capable of planning, implementing, debugging, verifying, and maintaining complete ROS 2 applications through collaborative AI agents with persistent memory and adaptive reasoning.

---

## License

MIT License.