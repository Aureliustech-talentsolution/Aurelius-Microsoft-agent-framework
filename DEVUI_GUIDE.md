# DevUI Guide
# Microsoft Agent Framework - Interactive Debug UI

**Version**: 1.0.0
**Date**: 2025-10-13
**Status**: Ready for Development

---

## 📖 What is DevUI?

**DevUI** is a lightweight, standalone sample app interface for running and testing agents and workflows in the Microsoft Agent Framework. It provides:

- 🌐 **Web-based UI** for interactive agent testing
- 🔌 **OpenAI-compatible API** server
- 🔍 **Directory-based discovery** of agents/workflows
- 📝 **In-memory entity registration**
- 🎨 **Sample entity gallery** with curated examples
- 📊 **OpenTelemetry tracing** for debugging

> **Important**: DevUI is a **sample app** for development and testing. It is **not intended for production use**. For production deployments, build your own custom interface and API server using the Agent Framework SDK.

---

## 🚀 Quick Start

### 1. Install DevUI

```bash
# DevUI is included when you install the full framework
cd python
uv pip install -e .[all]

# Or install just DevUI package
pip install agent-framework-devui --pre
```

### 2. Launch DevUI

#### Option A: Using VS Code Tasks (Recommended)

```
Ctrl+Shift+P → Tasks: Run Task → "DevUI: Start Server (Default Port 8080)"
```

Available tasks:
- `DevUI: Start Server (Default Port 8080)`
- `DevUI: Start Server (Custom Directory)`
- `DevUI: Start with Tracing (Framework)`
- `DevUI: Start with Tracing (All)`
- `DevUI: Start Headless (API Only)`
- `DevUI: Start with Auto-Reload`
- `DevUI: Test API Endpoints`
- `DevUI: Open in Browser`

#### Option B: Command Line

```bash
# Basic - discover agents in a directory
devui ./python/samples/getting_started/devui --port 8080

# With tracing enabled
devui ./python/samples/getting_started/devui --port 8080 --tracing framework

# Headless mode (API only, no web UI)
devui ./python/samples/getting_started/devui --port 8080 --headless

# With auto-reload for development
devui ./python/samples/getting_started/devui --port 8080 --reload
```

#### Option C: Programmatic Launch

```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from agent_framework.devui import serve

def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 72°F and sunny"

# Create your agent
agent = ChatAgent(
    name="WeatherAgent",
    chat_client=OpenAIChatClient(),
    tools=[get_weather]
)

# Launch DevUI - that's it!
serve(entities=[agent], auto_open=True)
# → Opens browser to http://localhost:8080
```

### 3. Access DevUI

Once started, DevUI is available at:
- **Web UI**: http://localhost:8080
- **API**: http://localhost:8080/v1/*
- **Health Check**: http://localhost:8080/health

---

## 🐛 Debugging DevUI

### Using VS Code Debug Configurations

DevUI includes 4 debug configurations (press F5 or use Run panel):

#### 1. **DevUI: Debug Server**
Launches DevUI server with debugger attached at default sample location.

```json
{
  "name": "DevUI: Debug Server",
  "module": "agent_framework_devui",
  "args": ["python/samples/getting_started/devui", "--port", "8080"]
}
```

#### 2. **DevUI: Debug with Tracing**
Launches DevUI with framework-level tracing enabled.

```json
{
  "name": "DevUI: Debug with Tracing",
  "args": [
    "python/samples/getting_started/devui",
    "--port", "8080",
    "--tracing", "framework"
  ]
}
```

#### 3. **DevUI: Debug Custom Directory**
Prompts for directory and port, then launches with debugger.

```json
{
  "name": "DevUI: Debug Custom Directory",
  "args": ["${input:devuiDirectory}", "--port", "${input:devuiPort}"]
}
```

#### 4. **DevUI: Debug In-Memory Mode**
Debugs the in-memory mode example directly.

```json
{
  "name": "DevUI: Debug In-Memory Mode",
  "program": "python/samples/getting_started/devui/in_memory_mode.py"
}
```

### How to Debug

1. **Set Breakpoints**: Click in the left gutter next to line numbers
2. **Start Debugging**: Press F5 and select a DevUI debug configuration
3. **Interact**: Use the web UI at http://localhost:8080
4. **Step Through**: Use F10 (step over), F11 (step into)
5. **Inspect**: Hover over variables or use the Variables panel

---

## 📁 Directory Structure

For agents/workflows to be discovered by DevUI, organize them like this:

```
agents/
├── weather_agent/
│   ├── __init__.py      # Must export: agent = ChatAgent(...)
│   ├── agent.py         # Your agent implementation
│   └── .env             # Optional: API keys, config vars
├── my_workflow/
│   ├── __init__.py      # Must export: workflow = WorkflowBuilder()...
│   ├── workflow.py      # Your workflow implementation
│   └── .env             # Optional: environment variables
└── .env                 # Optional: shared environment variables
```

### Example `__init__.py` for Agent

```python
# weather_agent/__init__.py
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 72°F and sunny"

agent = ChatAgent(
    name="WeatherAgent",
    chat_client=OpenAIChatClient(),
    instructions="You are a helpful weather assistant.",
    tools=[get_weather]
)
```

### Example `__init__.py` for Workflow

```python
# my_workflow/__init__.py
from agent_framework import WorkflowBuilder

workflow = (
    WorkflowBuilder()
    .add_node("step1", my_agent)
    .add_node("step2", another_agent)
    .add_edge("step1", "step2")
    .build()
)
```

---

## 🔌 OpenAI-Compatible API

DevUI provides an OpenAI Responses backend API. This means you can use the **OpenAI Python SDK** to interact with your agents!

### Basic Usage

```bash
# Using curl
curl -X POST http://localhost:8080/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "weather_agent",
    "input": "What'\''s the weather in Seattle?"
  }'
```

### Using OpenAI SDK

```python
from openai import OpenAI

# Connect to DevUI
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"  # API key not required for local DevUI
)

# Use your agent name as the model
response = client.responses.create(
    model="weather_agent",  # Your agent/workflow name
    input="What's the weather in Seattle?"
)

# Extract text
print(response.output[0].content[0].text)

# Streaming support
stream = client.responses.create(
    model="weather_agent",
    input="Tell me a long story",
    stream=True
)

for chunk in stream:
    if chunk.output:
        print(chunk.output[0].content[0].text, end="", flush=True)
```

### Multi-Turn Conversations

```python
# Create a conversation
conversation = client.conversations.create(
    metadata={"agent_id": "weather_agent"}
)

# First turn
response1 = client.responses.create(
    model="weather_agent",
    input="What's the weather in Seattle?",
    conversation=conversation.id
)

# Second turn - context is maintained!
response2 = client.responses.create(
    model="weather_agent",
    input="How about tomorrow?",  # Continues the conversation
    conversation=conversation.id
)
```

**How it works**: DevUI automatically retrieves the conversation's message history and passes it to the agent. You don't need to manually manage message history!

---

## 🔍 Viewing Telemetry (OpenTelemetry Traces)

DevUI can display OpenTelemetry traces for debugging agent behavior.

### Enable Tracing

```bash
# Framework-level tracing
devui ./agents --tracing framework

# Workflow-level tracing
devui ./agents --tracing workflow

# All tracing
devui ./agents --tracing all
```

### Using the Task

```
Ctrl+Shift+P → Tasks: Run Task → "DevUI: Start with Tracing (Framework)"
```

### What You Can See

- **Agent execution steps**: Each agent run and its sub-steps
- **Tool calls**: Function calls made by agents
- **LLM requests**: Calls to the language model
- **Workflow nodes**: Execution flow through workflow graph
- **Performance timing**: Duration of each operation

### Traces in the UI

1. Start DevUI with tracing enabled
2. Run an agent through the web UI
3. Click the "Traces" tab
4. View detailed execution timeline

---

## 📡 API Endpoints

### Entity Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/entities` | GET | List all discovered agents/workflows |
| `/v1/entities/{entity_id}/info` | GET | Get detailed entity information |
| `/v1/entities/add` | POST | Add entity from URL (gallery samples) |
| `/v1/entities/{entity_id}` | DELETE | Remove remote entity |

### Execution (OpenAI Responses API)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/responses` | POST | Execute agent/workflow (streaming or sync) |

### Conversations (OpenAI Standard)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/conversations` | POST | Create conversation |
| `/v1/conversations/{id}` | GET | Get conversation |
| `/v1/conversations/{id}` | POST | Update conversation metadata |
| `/v1/conversations/{id}` | DELETE | Delete conversation |
| `/v1/conversations?agent_id={id}` | GET | List conversations (DevUI extension) |
| `/v1/conversations/{id}/items` | POST | Add items to conversation |
| `/v1/conversations/{id}/items` | GET | List conversation items |
| `/v1/conversations/{id}/items/{item_id}` | GET | Get conversation item |

### Health Check

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check (returns 200 OK) |

### Test API Endpoints

```bash
# Using the task
Ctrl+Shift+P → Tasks: Run Task → "DevUI: Test API Endpoints"

# Or manually
curl http://localhost:8080/health
curl http://localhost:8080/v1/entities
```

---

## 🎨 Sample Gallery

When DevUI starts with no discovered entities, it displays a **sample entity gallery** with curated examples from the Agent Framework repository.

Features:
- ✅ One-click sample loading
- ✅ Pre-configured agents and workflows
- ✅ Examples for various use cases
- ✅ Learn by example approach

To use:
1. Start DevUI in an empty directory
2. Browse the sample gallery in the web UI
3. Click "Add" to load a sample
4. Test it immediately!

---

## ⚙️ CLI Options

```bash
devui [directory] [options]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `directory` | `.` | Directory to scan for agents/workflows |
| `--port, -p` | `8080` | Port to run server on |
| `--host` | `127.0.0.1` | Host to bind to |
| `--headless` | `False` | API only, no web UI |
| `--config` | None | YAML config file |
| `--tracing` | `none` | Tracing level: `none\|framework\|workflow\|all` |
| `--reload` | `False` | Enable auto-reload for development |

### Examples

```bash
# Basic usage
devui ./agents

# Custom port
devui ./agents --port 3000

# API only (no UI)
devui ./agents --headless

# With tracing and auto-reload
devui ./agents --tracing framework --reload

# Specific host
devui ./agents --host 0.0.0.0 --port 8080
```

---

## 🔧 Configuration File

You can use a YAML config file instead of CLI arguments:

```yaml
# devui-config.yaml
port: 8080
host: 127.0.0.1
headless: false
tracing: framework
reload: true
```

Launch with config:
```bash
devui ./agents --config devui-config.yaml
```

---

## 💡 Use Cases

### 1. **Local Agent Development**

```bash
# Start DevUI with auto-reload
devui ./my-agents --port 8080 --reload

# Edit your agent code
# → DevUI automatically reloads
# → Test changes immediately in the UI
```

### 2. **Debugging Agent Behavior**

```python
# Set breakpoints in your agent code
# Start debugging with F5 (DevUI: Debug Server)
# Interact through the web UI
# Step through code to find issues
```

### 3. **API Integration Testing**

```bash
# Start DevUI headless (API only)
devui ./agents --headless --port 8080

# Test with curl or Postman
curl -X POST http://localhost:8080/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"model": "my_agent", "input": "Hello"}'
```

### 4. **Workflow Visualization**

```bash
# Start with workflow tracing
devui ./workflows --tracing workflow

# Run a workflow through the UI
# View execution flow in traces
# Debug node-by-node execution
```

### 5. **Team Collaboration**

```bash
# Bind to network interface
devui ./agents --host 0.0.0.0 --port 8080

# Team members can access at:
# http://<your-ip>:8080
```

---

## 🚨 Troubleshooting

### DevUI Won't Start

**Problem**: Port already in use
```
Error: Address already in use: 127.0.0.1:8080
```

**Solution**: Use a different port
```bash
devui ./agents --port 8081
```

**Or find and kill the process**:
```bash
# Windows
netstat -ano | findstr :8080
taskkill /PID <pid> /F

# Linux/Mac
lsof -ti:8080 | xargs kill -9
```

### No Agents Discovered

**Problem**: DevUI shows "No entities found"

**Checklist**:
- ✅ Directory has `__init__.py` files in agent folders
- ✅ `__init__.py` exports `agent` or `workflow` variable
- ✅ No Python syntax errors in agent code
- ✅ Environment variables set (if needed)

**Debug**:
```bash
# Check directory structure
ls -R ./agents

# Verify __init__.py exports
python -c "from agents.my_agent import agent; print(agent)"
```

### API Calls Failing

**Problem**: 404 or 500 errors from API

**Solution**:
1. Check DevUI is running: `curl http://localhost:8080/health`
2. List entities: `curl http://localhost:8080/v1/entities`
3. Use exact entity name in API calls
4. Check DevUI terminal for error messages

### Tracing Not Showing

**Problem**: No traces visible in UI

**Solution**:
1. Ensure tracing enabled: `--tracing framework`
2. Check OpenTelemetry is configured
3. Run an agent to generate traces
4. Click "Traces" tab in UI

---

## 📚 Examples

### Complete Working Examples

Located in: `python/samples/getting_started/devui/`

#### 1. **In-Memory Mode** (`in_memory_mode.py`)
Register agents programmatically without file system discovery.

#### 2. **Weather Agent** (`weather_agent/`)
Simple agent with tool calling.

#### 3. **Foundry Agent** (`foundry_agent/`)
Azure AI Foundry integration example.

#### 4. **Spam Workflow** (`spam_workflow/`)
Multi-agent workflow example.

#### 5. **Workflow with Agents** (`workflow_agents/`)
Complex workflow with multiple agent nodes.

---

## 🎯 Best Practices

### 1. **Use .env Files**

```bash
# agents/my_agent/.env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
```

DevUI automatically loads `.env` files from:
- Agent/workflow directory
- Parent entities directory
- Current working directory

### 2. **Descriptive Agent Names**

```python
# Good
agent = ChatAgent(name="CustomerSupportAgent", ...)

# Bad
agent = ChatAgent(name="agent1", ...)
```

### 3. **Add Instructions**

```python
agent = ChatAgent(
    name="WeatherAgent",
    instructions="""
    You are a helpful weather assistant.
    - Provide accurate weather information
    - Include temperature, conditions, and forecasts
    - Be friendly and conversational
    """,
    tools=[get_weather]
)
```

### 4. **Use Type Hints**

```python
from typing import Annotated
from pydantic import Field

def get_weather(
    location: Annotated[str, Field(description="City name or zip code")],
    units: Annotated[str, Field(description="Temperature units: celsius or fahrenheit")] = "fahrenheit"
) -> str:
    """Get current weather for a location."""
    # Implementation
```

### 5. **Test Locally First**

```bash
# Use auto-reload during development
devui ./agents --reload --tracing framework

# Test in browser and via API
# Debug with breakpoints
# Verify tracing works
```

---

## 🔗 Related Documentation

- **[WORKSPACE_GUIDE.md](WORKSPACE_GUIDE.md)**: Complete workspace documentation
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Quick command reference
- **DevUI Package**: [python/packages/devui/README.md](python/packages/devui/README.md)
- **DevUI Samples**: [python/samples/getting_started/devui/](python/samples/getting_started/devui/)
- **Agent Framework Docs**: https://learn.microsoft.com/agent-framework/

---

## 🎉 You're Ready!

DevUI is now configured in your workspace with:

✅ **8 VS Code tasks** for easy launching
✅ **4 debug configurations** for debugging
✅ **OpenAI-compatible API** for integration testing
✅ **Tracing support** for observability
✅ **Sample gallery** for learning
✅ **Auto-reload** for development
✅ **Complete documentation**

**Start DevUI now:**
```
Ctrl+Shift+P → Tasks: Run Task → "DevUI: Start Server (Default Port 8080)"
```

**Or debug with F5:**
```
Run → DevUI: Debug Server
```

---

**Last Updated**: 2025-10-13
**Version**: 1.0.0
