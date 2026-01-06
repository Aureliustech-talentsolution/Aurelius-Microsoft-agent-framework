# Microsoft Agent Framework - SME Skills Guide

> **Comprehensive Subject Matter Expert Skills for Building Production-Level AI Agents**
>
> This document provides SME-level mastery skills for leveraging the Microsoft Agent Framework to create production-ready AI agents. It covers Python and .NET SDKs, workflow orchestration, tool integration, memory management, and observability.

---

## Table of Contents

1. [Framework Overview](#1-framework-overview)
2. [Python SDK Mastery](#2-python-sdk-mastery)
3. [.NET SDK Mastery](#3-net-sdk-mastery)
4. [Workflow Orchestration](#4-workflow-orchestration)
5. [Tool and Function Integration](#5-tool-and-function-integration)
6. [Memory and Context Management](#6-memory-and-context-management)
7. [Observability and Production Operations](#7-observability-and-production-operations)
8. [Production Deployment Patterns](#8-production-deployment-patterns)
9. [Quick Reference Cheatsheets](#9-quick-reference-cheatsheets)

---

## 1. Framework Overview

### 1.1 Architecture Principles

The Microsoft Agent Framework is built on these core principles:

| Principle | Description |
|-----------|-------------|
| **Protocol-Driven** | Interfaces define contracts; implementations are swappable |
| **Composable** | Small, focused components combine into complex behaviors |
| **Observable** | Built-in telemetry, tracing, and event emission |
| **Multi-Runtime** | Python and .NET SDKs with consistent patterns |
| **Workflow-Native** | DAG-based orchestration with checkpointing |

### 1.2 Component Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Agents    │  │  Workflows  │  │   Orchestrators         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                      CAPABILITY LAYER                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Tools     │  │   Memory    │  │   Context Providers     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                      INFRASTRUCTURE LAYER                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Chat Client │  │  Threading  │  │   Telemetry             │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Python SDK Mastery

### 2.1 Core Agent Architecture

#### Agent Type Hierarchy

```python
# Protocol definition (base contract)
class AgentProtocol(Protocol):
    """Base protocol all agents implement."""
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...

# Chat-capable agents
class ChatAgentProtocol(AgentProtocol, Protocol):
    """Protocol for agents that can participate in chat."""
    async def invoke(
        self,
        thread: AgentThread,
        options: ChatAgentOptions | None = None
    ) -> AsyncIterable[ChatMessage]: ...

    async def invoke_stream(
        self,
        thread: AgentThread,
        options: ChatAgentOptions | None = None
    ) -> AsyncIterable[ChatMessage]: ...
```

#### ChatAgent Implementation Pattern

```python
from agent_framework import ChatAgent, ChatClientProtocol, AgentThread
from agent_framework.tools import AIFunction

class ProductionAgent(ChatAgent):
    """Production-ready agent with full capabilities."""

    def __init__(
        self,
        client: ChatClientProtocol,
        name: str = "ProductionAgent",
        description: str = "A production-grade AI agent",
        instructions: str = "You are a helpful assistant.",
        tools: list[AIFunction] | None = None,
        context_providers: list[ContextProvider] | None = None,
    ):
        super().__init__(
            client=client,
            name=name,
            description=description,
            instructions=instructions,
            tools=tools or [],
            context_providers=context_providers or [],
        )

    # Override for custom pre-processing
    async def _pre_invoke(self, thread: AgentThread) -> None:
        """Called before each invocation."""
        await super()._pre_invoke(thread)
        # Custom initialization logic

    # Override for custom post-processing
    async def _post_invoke(self, thread: AgentThread) -> None:
        """Called after each invocation."""
        await super()._post_invoke(thread)
        # Custom cleanup logic
```

### 2.2 Client Configuration

#### OpenAI Client Setup

```python
from agent_framework.clients.openai import OpenAIChatClient

# Basic configuration
client = OpenAIChatClient(
    model="gpt-4o",
    api_key="your-api-key",  # Or use OPENAI_API_KEY env var
)

# Advanced configuration with custom settings
client = OpenAIChatClient(
    model="gpt-4o",
    api_key="your-api-key",
    temperature=0.7,
    max_tokens=4096,
    timeout=30.0,
    max_retries=3,
)
```

#### Azure OpenAI Client Setup

```python
from agent_framework.clients.azure_openai import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential

# Using API key
client = AzureOpenAIChatClient(
    deployment_name="gpt-4o-deployment",
    endpoint="https://your-resource.openai.azure.com",
    api_key="your-api-key",
    api_version="2024-02-15-preview",
)

# Using Azure Identity (recommended for production)
client = AzureOpenAIChatClient(
    deployment_name="gpt-4o-deployment",
    endpoint="https://your-resource.openai.azure.com",
    credential=DefaultAzureCredential(),
    api_version="2024-02-15-preview",
)
```

#### Anthropic Client Setup

```python
from agent_framework.clients.anthropic import AnthropicChatClient

client = AnthropicChatClient(
    model="claude-3-5-sonnet-20241022",
    api_key="your-api-key",  # Or use ANTHROPIC_API_KEY env var
)
```

### 2.3 Thread and Message Management

#### Thread Lifecycle

```python
from agent_framework import AgentThread, ChatMessage

# Create a new thread
thread = AgentThread()

# Add user message
thread.add_message(ChatMessage.user("Hello, how can you help me?"))

# Invoke agent and get response
async for message in agent.invoke(thread):
    print(f"{message.role}: {message.content}")

# Thread persists conversation history
print(f"Thread has {len(thread.messages)} messages")
```

#### Persistent Message Store

```python
from agent_framework.stores import RedisChatMessageStore
import redis.asyncio as redis

# Create Redis connection
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Create persistent store
store = RedisChatMessageStore(client=redis_client)

# Create thread with persistent storage
thread = AgentThread(message_store=store, thread_id="user-123-session-456")

# Messages automatically persist across sessions
await thread.add_message(ChatMessage.user("Remember this conversation"))
```

### 2.4 Instructions and System Prompts

#### Static Instructions

```python
agent = ChatAgent(
    client=client,
    instructions="""You are a customer support agent for TechCorp.

Your responsibilities:
1. Answer product questions accurately
2. Help troubleshoot common issues
3. Escalate complex problems to human agents

Always be professional and empathetic."""
)
```

#### Dynamic Instructions with Context

```python
from agent_framework import ContextProvider, ContextProviderConfig

class CustomerContextProvider(ContextProvider):
    """Injects customer-specific context into instructions."""

    def __init__(self, customer_service):
        self.customer_service = customer_service
        self.config = ContextProviderConfig(name="customer_context")

    async def invoking(self, context: dict) -> str:
        customer_id = context.get("customer_id")
        if customer_id:
            customer = await self.customer_service.get_customer(customer_id)
            return f"""
Customer Context:
- Name: {customer.name}
- Account Type: {customer.account_type}
- Support Tier: {customer.support_tier}
- Recent Orders: {customer.recent_orders}
"""
        return ""

# Use with agent
agent = ChatAgent(
    client=client,
    instructions="You are a personalized support agent.",
    context_providers=[CustomerContextProvider(customer_service)],
)
```

---

## 3. .NET SDK Mastery

### 3.1 Agent Architecture

#### Base Agent Pattern

```csharp
using Microsoft.AI.Agents;
using Microsoft.AI.ChatClient;

// Abstract base class for all agents
public abstract class AIAgent
{
    public abstract string Name { get; }
    public abstract string Description { get; }

    public abstract IAsyncEnumerable<ChatMessage> InvokeAsync(
        AgentThread thread,
        ChatAgentOptions? options = null,
        CancellationToken cancellationToken = default);

    public abstract IAsyncEnumerable<ChatMessage> InvokeStreamingAsync(
        AgentThread thread,
        ChatAgentOptions? options = null,
        CancellationToken cancellationToken = default);
}
```

#### ChatClientAgent Implementation

```csharp
using Microsoft.AI.Agents;
using Microsoft.Extensions.AI;

public class ProductionAgent : ChatClientAgent
{
    public override string Name => "ProductionAgent";
    public override string Description => "A production-grade .NET agent";

    public ProductionAgent(IChatClient chatClient) : base(chatClient)
    {
        Instructions = """
            You are a helpful AI assistant.
            Provide accurate and concise responses.
            """;
    }

    // Add custom tools
    public void ConfigureTools()
    {
        AddTool(AIFunctionFactory.Create(SearchDatabase));
        AddTool(AIFunctionFactory.Create(SendNotification));
    }

    [Description("Search the database for information")]
    private async Task<string> SearchDatabase(
        [Description("Search query")] string query)
    {
        // Implementation
        return $"Results for: {query}";
    }

    [Description("Send a notification to a user")]
    private async Task<string> SendNotification(
        [Description("User ID")] string userId,
        [Description("Message content")] string message)
    {
        // Implementation
        return "Notification sent";
    }
}
```

### 3.2 Builder Pattern

#### AIAgentBuilder Usage

```csharp
using Microsoft.AI.Agents.Builder;
using Microsoft.Extensions.AI;

// Fluent builder pattern
var agent = new AIAgentBuilder()
    .WithName("AssistantAgent")
    .WithDescription("A helpful assistant")
    .WithInstructions("""
        You are a helpful AI assistant.
        Be concise and accurate in your responses.
        """)
    .WithChatClient(chatClient)
    .WithTools(tools)
    .WithContextProviders(contextProviders)
    .Build();
```

#### Dependency Injection Integration

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.AI.Agents;

// In Startup.cs or Program.cs
services.AddAgentFramework(options =>
{
    options.DefaultModel = "gpt-4o";
    options.EnableTelemetry = true;
});

services.AddSingleton<IChatClient>(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    return new AzureOpenAIChatClient(
        endpoint: new Uri(config["AzureOpenAI:Endpoint"]),
        deploymentName: config["AzureOpenAI:DeploymentName"],
        credential: new DefaultAzureCredential());
});

services.AddTransient<ProductionAgent>();
```

### 3.3 Delegating Agent Pattern

```csharp
using Microsoft.AI.Agents;

/// <summary>
/// Wrapper pattern for adding cross-cutting concerns to agents.
/// </summary>
public class LoggingAgent : DelegatingAIAgent
{
    private readonly ILogger<LoggingAgent> _logger;

    public LoggingAgent(AIAgent innerAgent, ILogger<LoggingAgent> logger)
        : base(innerAgent)
    {
        _logger = logger;
    }

    public override async IAsyncEnumerable<ChatMessage> InvokeAsync(
        AgentThread thread,
        ChatAgentOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("Agent {Name} invoked with {MessageCount} messages",
            Name, thread.Messages.Count);

        var stopwatch = Stopwatch.StartNew();

        await foreach (var message in base.InvokeAsync(thread, options, cancellationToken))
        {
            yield return message;
        }

        _logger.LogInformation("Agent {Name} completed in {ElapsedMs}ms",
            Name, stopwatch.ElapsedMilliseconds);
    }
}

// Usage
var loggingAgent = new LoggingAgent(productionAgent, logger);
```

---

## 4. Workflow Orchestration

### 4.1 Workflow Fundamentals

The workflow system is inspired by Pregel (Google's graph processing model) and provides:
- **DAG-based execution** with typed nodes
- **Checkpointing** for fault tolerance
- **Human-in-the-loop** support
- **State management** across steps

#### Core Concepts

```
┌─────────────────────────────────────────────────────────────────┐
│                        WORKFLOW                                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │  START  │───▶│ Step 1  │───▶│ Step 2  │───▶│   END   │     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│                      │              ▲                           │
│                      │              │                           │
│                      ▼              │                           │
│                 ┌─────────┐        │                           │
│                 │ Step 3  │────────┘                           │
│                 └─────────┘                                     │
│                                                                 │
│  State: { current_step, accumulated_data, checkpoints }        │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Python Workflow Implementation

#### Basic Workflow Definition

```python
from agent_framework.workflows import (
    Workflow,
    WorkflowBuilder,
    Step,
    Edge,
    EdgeType,
)

# Define workflow state
@dataclass
class ResearchWorkflowState:
    query: str = ""
    search_results: list[str] = field(default_factory=list)
    analysis: str = ""
    final_report: str = ""

# Define steps
async def search_step(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Search for information."""
    # Perform search
    results = await search_service.search(state.query)
    state.search_results = results
    return state

async def analyze_step(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Analyze search results."""
    analysis = await analysis_agent.analyze(state.search_results)
    state.analysis = analysis
    return state

async def report_step(state: ResearchWorkflowState) -> ResearchWorkflowState:
    """Generate final report."""
    report = await report_agent.generate(state.analysis)
    state.final_report = report
    return state

# Build workflow
workflow = (
    WorkflowBuilder[ResearchWorkflowState]()
    .add_step("search", search_step)
    .add_step("analyze", analyze_step)
    .add_step("report", report_step)
    .add_edge("search", "analyze")
    .add_edge("analyze", "report")
    .set_entry_point("search")
    .build()
)

# Execute workflow
initial_state = ResearchWorkflowState(query="AI agent frameworks")
result = await workflow.run(initial_state)
print(result.final_report)
```

#### Conditional Branching

```python
from agent_framework.workflows import ConditionalEdge

def route_by_complexity(state: WorkflowState) -> str:
    """Route based on task complexity."""
    if state.complexity_score > 0.8:
        return "complex_handler"
    elif state.complexity_score > 0.5:
        return "medium_handler"
    else:
        return "simple_handler"

workflow = (
    WorkflowBuilder[WorkflowState]()
    .add_step("classifier", classify_step)
    .add_step("simple_handler", simple_step)
    .add_step("medium_handler", medium_step)
    .add_step("complex_handler", complex_step)
    .add_step("finalizer", finalize_step)
    .add_conditional_edge(
        "classifier",
        route_by_complexity,
        {
            "simple_handler": "simple_handler",
            "medium_handler": "medium_handler",
            "complex_handler": "complex_handler",
        }
    )
    .add_edge("simple_handler", "finalizer")
    .add_edge("medium_handler", "finalizer")
    .add_edge("complex_handler", "finalizer")
    .set_entry_point("classifier")
    .build()
)
```

#### Human-in-the-Loop

```python
from agent_framework.workflows import HumanInterrupt

async def approval_step(state: WorkflowState) -> WorkflowState:
    """Step requiring human approval."""
    if state.requires_approval:
        raise HumanInterrupt(
            message="Please review and approve the proposed action",
            data={"action": state.proposed_action},
            resume_step="execute_action"
        )
    return state

# Handle interrupt in application
try:
    result = await workflow.run(initial_state)
except HumanInterrupt as interrupt:
    # Present to user for approval
    approval = await get_user_approval(interrupt.message, interrupt.data)

    if approval:
        # Resume workflow from checkpoint
        result = await workflow.resume(
            interrupt.resume_step,
            state_with_approval
        )
```

### 4.3 Executor Types

#### Agent Executor

```python
from agent_framework.workflows import AgentExecutor

# Wrap agent as workflow step
agent_executor = AgentExecutor(
    agent=research_agent,
    input_mapper=lambda state: state.current_query,
    output_mapper=lambda state, response: state.update(research_result=response),
)

workflow = (
    WorkflowBuilder()
    .add_step("research", agent_executor)
    .build()
)
```

#### Function Executor

```python
from agent_framework.workflows import FunctionExecutor

async def process_data(data: dict) -> dict:
    """Pure function for data processing."""
    return {"processed": transform(data)}

function_executor = FunctionExecutor(
    func=process_data,
    input_mapper=lambda state: {"data": state.raw_data},
    output_mapper=lambda state, result: state.update(processed_data=result["processed"]),
)
```

#### Nested Workflow Executor

```python
from agent_framework.workflows import WorkflowExecutor

# Create sub-workflow
sub_workflow = create_data_processing_workflow()

# Embed in parent workflow
workflow_executor = WorkflowExecutor(
    workflow=sub_workflow,
    input_mapper=lambda state: SubWorkflowState(data=state.input_data),
    output_mapper=lambda state, sub_result: state.update(processed=sub_result.output),
)

parent_workflow = (
    WorkflowBuilder()
    .add_step("preprocess", preprocess_step)
    .add_step("sub_workflow", workflow_executor)
    .add_step("postprocess", postprocess_step)
    .add_edge("preprocess", "sub_workflow")
    .add_edge("sub_workflow", "postprocess")
    .build()
)
```

### 4.4 .NET Workflow Implementation

```csharp
using Microsoft.AI.Agents.Workflows;

// Define workflow state
public record ResearchState
{
    public string Query { get; init; } = "";
    public List<string> SearchResults { get; init; } = new();
    public string Analysis { get; init; } = "";
    public string Report { get; init; } = "";
}

// Build workflow
var workflow = new WorkflowBuilder<ResearchState>()
    .AddStep("search", async (state, ct) =>
    {
        var results = await searchService.SearchAsync(state.Query, ct);
        return state with { SearchResults = results };
    })
    .AddStep("analyze", async (state, ct) =>
    {
        var analysis = await analyzer.AnalyzeAsync(state.SearchResults, ct);
        return state with { Analysis = analysis };
    })
    .AddStep("report", async (state, ct) =>
    {
        var report = await reporter.GenerateAsync(state.Analysis, ct);
        return state with { Report = report };
    })
    .AddEdge("search", "analyze")
    .AddEdge("analyze", "report")
    .SetEntryPoint("search")
    .Build();

// Execute
var result = await workflow.RunAsync(new ResearchState { Query = "AI agents" });
```

---

## 5. Tool and Function Integration

### 5.1 AIFunction Decorator Pattern

#### Basic Tool Definition

```python
from agent_framework.tools import ai_function

@ai_function
async def search_database(
    query: str,
    limit: int = 10,
    filters: dict[str, str] | None = None
) -> list[dict]:
    """
    Search the database for records matching the query.

    Args:
        query: Search query string
        limit: Maximum number of results to return
        filters: Optional filters to apply

    Returns:
        List of matching records
    """
    # Implementation
    results = await db.search(query, limit=limit, filters=filters or {})
    return [record.to_dict() for record in results]
```

#### Tool with Complex Types

```python
from pydantic import BaseModel, Field
from agent_framework.tools import ai_function

class OrderDetails(BaseModel):
    """Details for creating an order."""
    product_id: str = Field(description="Product identifier")
    quantity: int = Field(ge=1, description="Quantity to order")
    shipping_address: str = Field(description="Delivery address")
    express_shipping: bool = Field(default=False, description="Use express shipping")

class OrderResult(BaseModel):
    """Result of order creation."""
    order_id: str
    estimated_delivery: str
    total_cost: float

@ai_function
async def create_order(details: OrderDetails) -> OrderResult:
    """
    Create a new order in the system.

    Args:
        details: Order details including product, quantity, and shipping

    Returns:
        Order confirmation with ID, delivery estimate, and cost
    """
    order = await order_service.create(
        product_id=details.product_id,
        quantity=details.quantity,
        address=details.shipping_address,
        express=details.express_shipping
    )
    return OrderResult(
        order_id=order.id,
        estimated_delivery=order.estimated_delivery.isoformat(),
        total_cost=order.total
    )
```

### 5.2 MCP (Model Context Protocol) Integration

#### Stdio MCP Tool

```python
from agent_framework.tools.mcp import MCPStdioTool

# Connect to MCP server via stdio
filesystem_tool = MCPStdioTool(
    command="npx",
    args=["-y", "@anthropic/mcp-filesystem"],
    env={"ALLOWED_PATHS": "/data,/config"},
)

# Use with agent
agent = ChatAgent(
    client=client,
    tools=[filesystem_tool],
)
```

#### HTTP MCP Tool

```python
from agent_framework.tools.mcp import MCPHttpTool

# Connect to HTTP-based MCP server
api_tool = MCPHttpTool(
    url="https://mcp.example.com/api",
    headers={"Authorization": "Bearer token"},
    timeout=30.0,
)
```

#### WebSocket MCP Tool

```python
from agent_framework.tools.mcp import MCPWebSocketTool

# Connect to WebSocket MCP server for real-time capabilities
realtime_tool = MCPWebSocketTool(
    url="wss://mcp.example.com/ws",
    reconnect_attempts=3,
    ping_interval=30,
)
```

### 5.3 Hosted Tools

#### Code Interpreter

```python
from agent_framework.tools.hosted import CodeInterpreterTool

code_interpreter = CodeInterpreterTool(
    sandbox_type="docker",  # or "e2b", "modal"
    timeout=60,
    allowed_packages=["pandas", "numpy", "matplotlib"],
)

agent = ChatAgent(
    client=client,
    tools=[code_interpreter],
    instructions="You can execute Python code to analyze data.",
)
```

#### File Search (RAG)

```python
from agent_framework.tools.hosted import FileSearchTool
from agent_framework.vectorstores import AzureAISearchVectorStore

# Configure vector store
vector_store = AzureAISearchVectorStore(
    endpoint="https://search.example.com",
    index_name="documents",
    credential=DefaultAzureCredential(),
)

file_search = FileSearchTool(
    vector_store=vector_store,
    top_k=10,
    score_threshold=0.7,
)

agent = ChatAgent(
    client=client,
    tools=[file_search],
    instructions="Search the document repository to answer questions.",
)
```

#### Web Search

```python
from agent_framework.tools.hosted import BingSearchTool

web_search = BingSearchTool(
    api_key="your-bing-api-key",
    market="en-US",
    safe_search="moderate",
)

agent = ChatAgent(
    client=client,
    tools=[web_search],
    instructions="Search the web for current information.",
)
```

### 5.4 Tool Approval Workflow

#### Approval Handler Pattern

```python
from agent_framework.tools import ToolApprovalHandler, ApprovalDecision

class ProductionApprovalHandler(ToolApprovalHandler):
    """Production-grade tool approval with audit logging."""

    def __init__(self, audit_logger, notification_service):
        self.audit_logger = audit_logger
        self.notification_service = notification_service

    async def request_approval(
        self,
        tool_name: str,
        tool_args: dict,
        context: dict
    ) -> ApprovalDecision:
        """Request approval for tool execution."""

        # Log the request
        await self.audit_logger.log(
            event="tool_approval_requested",
            tool=tool_name,
            args=tool_args,
            user=context.get("user_id"),
        )

        # Check auto-approval rules
        if self._is_auto_approved(tool_name, tool_args, context):
            return ApprovalDecision(approved=True, reason="Auto-approved by policy")

        # Request human approval
        approval = await self.notification_service.request_approval(
            message=f"Approve {tool_name} execution?",
            details=tool_args,
            timeout=300,  # 5 minute timeout
        )

        return ApprovalDecision(
            approved=approval.granted,
            reason=approval.reason,
            modified_args=approval.modified_args,
        )

    def _is_auto_approved(self, tool_name: str, args: dict, context: dict) -> bool:
        """Check if tool call can be auto-approved."""
        # Read-only operations auto-approved
        if tool_name in ["search", "get_info", "list_items"]:
            return True
        # Low-value transactions auto-approved
        if tool_name == "create_order" and args.get("total", 0) < 100:
            return True
        return False
```

#### Using Approval Handler

```python
agent = ChatAgent(
    client=client,
    tools=[create_order, delete_record, modify_settings],
    tool_approval_handler=ProductionApprovalHandler(
        audit_logger=audit_logger,
        notification_service=notification_service,
    ),
)
```

### 5.5 .NET Tool Definition

```csharp
using Microsoft.Extensions.AI;

public class DatabaseTools
{
    private readonly IDbConnection _db;

    public DatabaseTools(IDbConnection db)
    {
        _db = db;
    }

    [Description("Search the database for records")]
    public async Task<List<Record>> SearchDatabase(
        [Description("Search query")] string query,
        [Description("Maximum results")] int limit = 10)
    {
        return await _db.SearchAsync(query, limit);
    }

    [Description("Get record by ID")]
    public async Task<Record?> GetRecord(
        [Description("Record identifier")] string id)
    {
        return await _db.GetByIdAsync(id);
    }
}

// Register tools with agent
var tools = AIFunctionFactory.Create(new DatabaseTools(db));
var agent = new AIAgentBuilder()
    .WithChatClient(chatClient)
    .WithTools(tools)
    .Build();
```

---

## 6. Memory and Context Management

### 6.1 Context Provider Architecture

#### Provider Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT PROVIDER LIFECYCLE                    │
│                                                                  │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │ Request │───▶│   invoking   │───▶│ Agent Runs   │           │
│  └─────────┘    │ (pre-invoke) │    │              │           │
│                 └──────────────┘    └──────────────┘           │
│                                            │                    │
│                                            ▼                    │
│                                     ┌──────────────┐           │
│                                     │   invoked    │           │
│                                     │ (post-invoke)│           │
│                                     └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

#### Custom Context Provider

```python
from agent_framework import ContextProvider, ContextProviderConfig

class ComprehensiveContextProvider(ContextProvider):
    """Production context provider with multiple data sources."""

    def __init__(
        self,
        user_service,
        preference_service,
        history_service,
    ):
        self.user_service = user_service
        self.preference_service = preference_service
        self.history_service = history_service
        self.config = ContextProviderConfig(
            name="comprehensive_context",
            priority=100,  # Higher priority = injected first
        )

    async def invoking(self, context: dict) -> str:
        """Inject context before agent invocation."""
        user_id = context.get("user_id")
        if not user_id:
            return ""

        # Fetch data in parallel
        user, preferences, history = await asyncio.gather(
            self.user_service.get(user_id),
            self.preference_service.get(user_id),
            self.history_service.get_recent(user_id, limit=5),
        )

        return f"""
=== User Context ===
User: {user.name} ({user.role})
Account Created: {user.created_at}
Preferences:
- Language: {preferences.language}
- Timezone: {preferences.timezone}
- Communication Style: {preferences.style}

Recent Interactions:
{self._format_history(history)}
"""

    async def invoked(self, context: dict, response: str) -> None:
        """Process after agent invocation (e.g., update history)."""
        user_id = context.get("user_id")
        if user_id:
            await self.history_service.add(
                user_id=user_id,
                interaction=response,
                timestamp=datetime.utcnow(),
            )

    def _format_history(self, history: list) -> str:
        return "\n".join(
            f"- [{h.timestamp}] {h.summary}"
            for h in history
        )
```

### 6.2 Memory Providers

#### Mem0 Integration

```python
from agent_framework.memory import Mem0Provider

# Configure Mem0 for long-term memory
memory_provider = Mem0Provider(
    api_key="your-mem0-api-key",
    user_id_extractor=lambda ctx: ctx.get("user_id"),
    memory_config={
        "retention_days": 90,
        "max_memories": 1000,
        "similarity_threshold": 0.8,
    },
)

agent = ChatAgent(
    client=client,
    context_providers=[memory_provider],
    instructions="You remember past conversations with users.",
)
```

#### Redis Memory Provider

```python
from agent_framework.memory import RedisContextProvider
import redis.asyncio as redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)

memory_provider = RedisContextProvider(
    client=redis_client,
    key_prefix="agent:memory:",
    ttl=3600 * 24 * 7,  # 7 days
    max_context_items=50,
)
```

### 6.3 Aggregate Context

```python
from agent_framework import AggregateContextProvider

# Combine multiple context providers
aggregate_provider = AggregateContextProvider(
    providers=[
        user_context_provider,      # Priority 100
        memory_provider,            # Priority 90
        preferences_provider,       # Priority 80
        recent_activity_provider,   # Priority 70
    ],
    separator="\n---\n",
)

agent = ChatAgent(
    client=client,
    context_providers=[aggregate_provider],
)
```

### 6.4 .NET Context Provider

```csharp
using Microsoft.AI.Agents;

public class CustomerContextProvider : AIContextProvider
{
    private readonly ICustomerService _customerService;

    public CustomerContextProvider(ICustomerService customerService)
    {
        _customerService = customerService;
    }

    public override async Task<string> GetContextAsync(
        IDictionary<string, object> context,
        CancellationToken cancellationToken = default)
    {
        if (!context.TryGetValue("customerId", out var customerId))
            return string.Empty;

        var customer = await _customerService.GetAsync(
            customerId.ToString()!,
            cancellationToken);

        return $"""
            Customer: {customer.Name}
            Account Type: {customer.AccountType}
            Support Tier: {customer.SupportTier}
            """;
    }
}
```

---

## 7. Observability and Production Operations

### 7.1 OpenTelemetry Integration

#### Python Setup

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from agent_framework.telemetry import configure_telemetry

# Configure OpenTelemetry
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://collector:4317"))
)

metrics.set_meter_provider(MeterProvider())

# Enable agent framework telemetry
configure_telemetry(
    service_name="production-agent",
    enable_tracing=True,
    enable_metrics=True,
    log_level="INFO",
)
```

#### Semantic Conventions for GenAI

```python
# The framework follows OpenTelemetry Semantic Conventions for GenAI
# Spans include these attributes:

# gen_ai.system: "openai" | "azure_openai" | "anthropic"
# gen_ai.request.model: "gpt-4o"
# gen_ai.request.max_tokens: 4096
# gen_ai.request.temperature: 0.7
# gen_ai.response.model: "gpt-4o-2024-08-06"
# gen_ai.usage.input_tokens: 150
# gen_ai.usage.output_tokens: 500
# gen_ai.response.finish_reason: "stop"
```

### 7.2 Lifecycle Events

#### Event Emitter Pattern

```python
from agent_framework.events import LifecycleEventEmitter, AgentEvent

class ProductionEventHandler:
    """Handle agent lifecycle events for monitoring."""

    def __init__(self, metrics_client, alert_service):
        self.metrics_client = metrics_client
        self.alert_service = alert_service

    async def on_agent_start(self, event: AgentEvent):
        """Called when agent invocation starts."""
        self.metrics_client.increment("agent.invocations.started")

    async def on_agent_complete(self, event: AgentEvent):
        """Called when agent invocation completes."""
        self.metrics_client.increment("agent.invocations.completed")
        self.metrics_client.histogram(
            "agent.invocation.duration",
            event.duration_ms
        )
        self.metrics_client.histogram(
            "agent.tokens.used",
            event.total_tokens
        )

    async def on_agent_error(self, event: AgentEvent):
        """Called when agent encounters an error."""
        self.metrics_client.increment("agent.invocations.failed")

        if event.error_type == "rate_limit":
            await self.alert_service.warn(
                "Rate limit hit",
                details={"agent": event.agent_name}
            )
        elif event.error_type == "timeout":
            await self.alert_service.alert(
                "Agent timeout",
                details={"agent": event.agent_name, "duration": event.duration_ms}
            )

    async def on_tool_call(self, event: AgentEvent):
        """Called when a tool is invoked."""
        self.metrics_client.increment(
            "agent.tool.calls",
            tags={"tool": event.tool_name}
        )

# Register handler
emitter = LifecycleEventEmitter()
handler = ProductionEventHandler(metrics_client, alert_service)

emitter.on("agent_start", handler.on_agent_start)
emitter.on("agent_complete", handler.on_agent_complete)
emitter.on("agent_error", handler.on_agent_error)
emitter.on("tool_call", handler.on_tool_call)

# Use with agent
agent = ChatAgent(
    client=client,
    event_emitter=emitter,
)
```

### 7.3 Azure Monitor Integration

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# Configure Azure Monitor
configure_azure_monitor(
    connection_string="InstrumentationKey=xxx;IngestionEndpoint=xxx"
)

# Traces, metrics, and logs automatically exported to Azure Monitor
# View in Azure Portal > Application Insights
```

### 7.4 Structured Logging

```python
import structlog
from agent_framework.logging import configure_logging

# Configure structured logging
configure_logging(
    level="INFO",
    format="json",  # or "console" for development
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger("agent")

# Logs include context automatically
logger.info(
    "agent_invoked",
    agent_name="ProductionAgent",
    user_id="user-123",
    thread_id="thread-456",
)
```

---

## 8. Production Deployment Patterns

### 8.1 Multi-Agent Orchestration

#### Sequential Orchestration

```python
from agent_framework.orchestration import SequentialOrchestrator

orchestrator = SequentialOrchestrator(
    agents=[
        classifier_agent,   # Classify the request
        router_agent,       # Route to specialist
        specialist_agent,   # Handle the request
        reviewer_agent,     # Review the response
    ],
    thread_sharing="shared",  # All agents see full conversation
)

result = await orchestrator.run(thread)
```

#### Parallel Orchestration

```python
from agent_framework.orchestration import ParallelOrchestrator

orchestrator = ParallelOrchestrator(
    agents=[
        research_agent,     # Research in parallel
        analysis_agent,     # Analyze in parallel
        validation_agent,   # Validate in parallel
    ],
    aggregator=consensus_aggregator,  # Combine results
)

result = await orchestrator.run(thread)
```

#### Hierarchical Orchestration

```python
from agent_framework.orchestration import HierarchicalOrchestrator

orchestrator = HierarchicalOrchestrator(
    supervisor=supervisor_agent,
    workers={
        "research": research_agent,
        "writing": writing_agent,
        "review": review_agent,
    },
    max_iterations=5,
)

# Supervisor delegates to workers based on task requirements
result = await orchestrator.run(thread)
```

### 8.2 Error Handling and Resilience

#### Retry Pattern

```python
from agent_framework.resilience import RetryPolicy, ExponentialBackoff

retry_policy = RetryPolicy(
    max_retries=3,
    backoff=ExponentialBackoff(
        initial_delay=1.0,
        max_delay=30.0,
        multiplier=2.0,
    ),
    retryable_errors=[
        "rate_limit_exceeded",
        "service_unavailable",
        "timeout",
    ],
)

agent = ChatAgent(
    client=client,
    retry_policy=retry_policy,
)
```

#### Circuit Breaker

```python
from agent_framework.resilience import CircuitBreaker

circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60.0,
    half_open_max_calls=3,
)

@circuit_breaker
async def call_agent(thread: AgentThread):
    return await agent.invoke(thread)
```

#### Fallback Pattern

```python
from agent_framework.resilience import FallbackChain

fallback_chain = FallbackChain(
    primary=gpt4_agent,
    fallbacks=[
        gpt35_agent,        # First fallback
        simple_response,    # Final fallback
    ],
    on_fallback=lambda e: logger.warning(f"Fallback triggered: {e}"),
)

result = await fallback_chain.invoke(thread)
```

### 8.3 Rate Limiting

```python
from agent_framework.resilience import TokenBucketRateLimiter

rate_limiter = TokenBucketRateLimiter(
    tokens_per_second=10,
    bucket_size=100,
)

async def invoke_with_rate_limit(thread: AgentThread):
    await rate_limiter.acquire()
    return await agent.invoke(thread)
```

### 8.4 Caching

```python
from agent_framework.caching import ResponseCache

cache = ResponseCache(
    backend=RedisCache(redis_client),
    ttl=3600,
    key_generator=lambda thread: hash(thread.messages[-1].content),
)

cached_agent = cache.wrap(agent)
# Identical queries return cached responses
```

### 8.5 Health Checks

```python
from agent_framework.health import HealthCheck, HealthStatus

class AgentHealthCheck(HealthCheck):
    def __init__(self, agent, test_prompt):
        self.agent = agent
        self.test_prompt = test_prompt

    async def check(self) -> HealthStatus:
        try:
            thread = AgentThread()
            thread.add_message(ChatMessage.user(self.test_prompt))

            start = time.time()
            async for _ in self.agent.invoke(thread):
                pass
            duration = time.time() - start

            return HealthStatus(
                healthy=True,
                latency_ms=duration * 1000,
                details={"model": self.agent.client.model},
            )
        except Exception as e:
            return HealthStatus(
                healthy=False,
                error=str(e),
            )

# Register health checks
health_registry.register("agent", AgentHealthCheck(agent, "ping"))
```

---

## 9. Quick Reference Cheatsheets

### 9.1 Python Agent Creation Cheatsheet

```python
# ===== MINIMAL AGENT =====
from agent_framework import ChatAgent
from agent_framework.clients.openai import OpenAIChatClient

agent = ChatAgent(
    client=OpenAIChatClient(model="gpt-4o"),
    instructions="You are a helpful assistant."
)

# ===== FULL-FEATURED AGENT =====
from agent_framework import ChatAgent, AgentThread, ContextProvider
from agent_framework.clients.azure_openai import AzureOpenAIChatClient
from agent_framework.tools import ai_function
from agent_framework.memory import Mem0Provider
from agent_framework.telemetry import configure_telemetry

# Configure telemetry
configure_telemetry(service_name="my-agent")

# Define tools
@ai_function
async def search(query: str) -> list[dict]:
    """Search for information."""
    return await search_service.search(query)

# Create client
client = AzureOpenAIChatClient(
    deployment_name="gpt-4o",
    endpoint="https://xxx.openai.azure.com",
    credential=DefaultAzureCredential(),
)

# Create agent
agent = ChatAgent(
    client=client,
    name="ProductionAgent",
    instructions="You are a production assistant.",
    tools=[search],
    context_providers=[Mem0Provider(api_key="xxx")],
)

# Use agent
thread = AgentThread()
thread.add_message(ChatMessage.user("Search for AI frameworks"))
async for message in agent.invoke(thread):
    print(message.content)
```

### 9.2 Workflow Creation Cheatsheet

```python
# ===== BASIC WORKFLOW =====
from agent_framework.workflows import WorkflowBuilder

workflow = (
    WorkflowBuilder()
    .add_step("step1", step1_func)
    .add_step("step2", step2_func)
    .add_edge("step1", "step2")
    .set_entry_point("step1")
    .build()
)

result = await workflow.run(initial_state)

# ===== CONDITIONAL WORKFLOW =====
workflow = (
    WorkflowBuilder()
    .add_step("classify", classify)
    .add_step("simple", simple_handler)
    .add_step("complex", complex_handler)
    .add_conditional_edge("classify", route_func, {
        "simple": "simple",
        "complex": "complex"
    })
    .set_entry_point("classify")
    .build()
)

# ===== WITH CHECKPOINTING =====
from agent_framework.workflows import RedisCheckpointer

checkpointer = RedisCheckpointer(redis_client)
workflow = WorkflowBuilder().with_checkpointer(checkpointer).build()
```

### 9.3 Tool Definition Cheatsheet

```python
# ===== BASIC TOOL =====
@ai_function
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression)  # Use safe eval in production

# ===== ASYNC TOOL =====
@ai_function
async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

# ===== TOOL WITH PYDANTIC =====
class SearchParams(BaseModel):
    query: str
    limit: int = 10
    filters: dict[str, str] = {}

@ai_function
async def search(params: SearchParams) -> list[dict]:
    """Search with parameters."""
    return await db.search(**params.dict())

# ===== MCP TOOL =====
from agent_framework.tools.mcp import MCPStdioTool

mcp_tool = MCPStdioTool(
    command="npx",
    args=["-y", "@anthropic/mcp-filesystem"]
)
```

### 9.4 Common Configuration Patterns

```python
# ===== ENVIRONMENT-BASED CONFIG =====
import os
from agent_framework.config import AgentConfig

config = AgentConfig(
    model=os.getenv("AGENT_MODEL", "gpt-4o"),
    temperature=float(os.getenv("AGENT_TEMPERATURE", "0.7")),
    max_tokens=int(os.getenv("AGENT_MAX_TOKENS", "4096")),
    timeout=float(os.getenv("AGENT_TIMEOUT", "30.0")),
)

# ===== YAML CONFIG =====
# config.yaml
# agent:
#   model: gpt-4o
#   temperature: 0.7
#   max_tokens: 4096

import yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)["agent"]

# ===== AZURE KEY VAULT =====
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

vault = SecretClient(
    vault_url="https://xxx.vault.azure.net",
    credential=DefaultAzureCredential()
)
api_key = vault.get_secret("openai-api-key").value
```

### 9.5 Testing Patterns

```python
# ===== UNIT TEST WITH MOCK CLIENT =====
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_client():
    client = AsyncMock()
    client.complete.return_value = ChatCompletion(
        content="Test response",
        usage=Usage(input_tokens=10, output_tokens=20)
    )
    return client

async def test_agent_invoke(mock_client):
    agent = ChatAgent(client=mock_client, instructions="Test")
    thread = AgentThread()
    thread.add_message(ChatMessage.user("Hello"))

    messages = [m async for m in agent.invoke(thread)]

    assert len(messages) == 1
    assert messages[0].content == "Test response"

# ===== INTEGRATION TEST =====
@pytest.mark.integration
async def test_agent_with_tools():
    agent = create_production_agent()
    thread = AgentThread()
    thread.add_message(ChatMessage.user("Search for Python tutorials"))

    messages = [m async for m in agent.invoke(thread)]

    assert any("Python" in m.content for m in messages)

# ===== WORKFLOW TEST =====
async def test_workflow_execution():
    workflow = create_test_workflow()
    initial_state = WorkflowState(input="test")

    result = await workflow.run(initial_state)

    assert result.completed
    assert result.output is not None
```

---

## Appendix A: Error Reference

| Error | Cause | Resolution |
|-------|-------|------------|
| `RateLimitExceeded` | Too many API calls | Implement retry with backoff |
| `ContextLengthExceeded` | Input too long | Truncate or summarize context |
| `ToolExecutionError` | Tool failed | Check tool implementation |
| `AuthenticationError` | Invalid credentials | Verify API keys/credentials |
| `TimeoutError` | Request too slow | Increase timeout or optimize |
| `WorkflowCheckpointError` | State save failed | Check checkpoint storage |

## Appendix B: Performance Optimization

| Optimization | Impact | Implementation |
|--------------|--------|----------------|
| Response caching | High | Redis-based ResponseCache |
| Connection pooling | Medium | Configure client pool size |
| Async tools | High | Use async/await in all tools |
| Streaming responses | Medium | Use invoke_stream() |
| Context pruning | High | Limit context provider output |
| Batch processing | High | Process multiple requests |

## Appendix C: Security Checklist

- [ ] API keys stored in secure vault (not environment variables)
- [ ] Tool inputs validated and sanitized
- [ ] Rate limiting enabled
- [ ] Audit logging for sensitive operations
- [ ] Tool approval workflow for destructive actions
- [ ] PII filtering in logs and telemetry
- [ ] Network isolation for MCP tools
- [ ] Regular credential rotation
- [ ] Input/output content filtering

---

*This skills guide was generated from comprehensive analysis of the Microsoft Agent Framework codebase. For the latest documentation, refer to the official repository.*
