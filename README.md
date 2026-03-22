# MCP Personal Trainer Agent

This project implements a **Personal Trainer AI Agent** connected to an **MCP (Model Context Protocol) server**.

The agent helps users with:

* Workout plans
* Daily workouts
* Meal planning

It uses:

* MCP tools
* Streaming responses
* Conversation memory
* Input validation before tool usage

---

#  Quick Start

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd mcp-personal-trainer-agent
```

---

## 2. Install dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

## 3. Setup environment variables

Create a `.env` file in the root:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## 4. Run the MCP Server

From server project:
https://github.com/Aleex87/mcp-personal-trainer-server


```bash
uv run python src/main.py
```

Server will run on:

```text
http://localhost:8001/mcp
```

---

## 5. Run the Agent

```bash
uv run python -m src.agent.main
```

---

#  How It Works

## Architecture Overview

```
User Input
   ↓
Agent (LangChain + Streaming)
   ↓
Tool Filtering Layer
   ↓
MCP Client
   ↓
MCP Server (FastMCP)
   ↓
Tools Execution
   ↓
Response back to Agent
```

---

# Features

##  MCP Integration

* Connects to MCP server via HTTP
* Retrieves tools dynamically

---

##  Tool Filtering (Required)

The agent only has access to a subset of tools:

```python
generate_workout_plan
get_daily_workout
generate_meal_plan
```

This enforces **least privilege access**.

---

##  Streaming Responses

The agent uses streaming:

```python
agent.astream(...)
```

Handled via:

```python
handle_stream_async(...)
```

---

##  Conversation Memory

* Stores last **10 exchanges (20 messages)**
* Improves contextual understanding
* Implemented in `memory.py`

---

#  Project Structure

```
src/
  agent/
    main.py          # Entry point
    agent.py         # Agent + MCP connection
    prompt.py        # System prompt (REPO framework)
    tool_filter.py   # Tool filtering
    memory.py        # Conversation memory
  shared/
    models.py        # LLM configuration

util/
  pretty_print.py
  streaming_utils.py
```

---

#  Design Decisions

##  Why Tool Filtering?

To ensure:

* Security
* Simplicity
* Controlled agent behavior

---

##  Why Input Validation?

LLMs tend to:

* Call tools too early
* Ignore missing information

Solution:

* Add a **system-level validation layer**

---

##  Why Memory Limiting?

Too much memory:

* Reduces prompt adherence
* Causes hallucinations

Solution:

* Keep only recent messages

---

##  Why Streaming?

Provides:

* Better UX
* Real-time feedback
* Required by assignment

---

#  Example Usage

```text
Ask something: I want to build muscle

Agent:
I need some more details:
- Age
- Weight
- Height
- Gender
- Fitness level

Ask something: 30, 80kg, 180cm, male, beginner

→ Tool is called
→ Workout plan is generated
```

---

##  Robust Input Parsing

The system handles flexible input:

- `38, 95, 187, male, beginner`
- `male beginner 187cm 95kg 38 years`
- `I am 38, 95kg, 187cm, beginner`

---

#  Commands

| Command | Description               |
| ------- | ------------------------- |
| exit    | Quit the program          |
| refresh | Clear conversation memory |

---

#  Concepts Used

* MCP (Model Context Protocol)
* Tool-based agents
* Streaming LLM responses
* Input validation layer
* Context memory management

---

#  Requirements Covered

✔ MCP server connection
✔ Tool filtering
✔ Middleware-like control (via validation layer)
✔ Structured prompt (REPO)
✔ Streaming responses
✔ Clean architecture

---

#  Final Notes

This project demonstrates how to:

* Build a safe and controlled AI agent
* Integrate external tools via MCP
* Prevent incorrect tool usage
* Manage conversation state effectively

---

# Author

Alessandro Abbate
