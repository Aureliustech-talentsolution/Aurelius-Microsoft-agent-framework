# Architecture Document
# Microsoft Agent Framework - Aurelius Implementation

**Version**: 1.0.0
**Date**: 2025-10-13
**Status**: Living Document
**Classification**: Unclassified // Technical

---

## Table of Contents
1. [System Overview](#1-system-overview)
2. [Architecture Principles](#2-architecture-principles)
3. [Component Architecture](#3-component-architecture)
4. [Security Architecture](#4-security-architecture)
5. [Data Architecture](#5-data-architecture)
6. [Integration Architecture](#6-integration-architecture)
7. [Deployment Architecture](#7-deployment-architecture)
8. [Observability Architecture](#8-observability-architecture)

---

## 1. System Overview

### 1.1 Architecture Vision
Build a secure, scalable, federally-compliant AI agent platform using Microsoft Agent Framework that enables rapid development and deployment of intelligent automation solutions for government and commercial clients.

### 1.2 Architecture Goals
- **Modularity**: Loosely coupled components with clear interfaces
- **Security**: Zero-trust architecture with defense-in-depth
- **Scalability**: Horizontal scaling for high-throughput scenarios
- **Resilience**: Fault tolerance with graceful degradation
- **Observability**: Complete visibility into system behavior
- **Compliance**: Built-in federal compliance controls

### 1.3 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                       │
│  (Web, Mobile, CLI, APIs, Power Platform Connectors)        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTPS/gRPC/WebSocket
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  API Gateway Layer                           │
│  (Azure API Management, Auth, Rate Limiting, Routing)       │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼────────┐ ┌▼────────────┐
│  Python      │ │  .NET      │ │  Workflow   │
│  Agents      │ │  Agents    │ │  Engine     │
│  Service     │ │  Service   │ │  Service    │
└───────┬──────┘ └──┬─────────┘ └┬────────────┘
        │           │             │
        └───────────┼─────────────┘
                    │
        ┌───────────┼───────────────┐
        │           │               │
┌───────▼──────┐ ┌─▼──────────┐ ┌─▼──────────┐
│  LLM         │ │  State      │ │  Context   │
│  Providers   │ │  Store      │ │  Providers │
│  (Multi)     │ │  (Redis)    │ │  (Mem0)    │
└──────────────┘ └─────────────┘ └────────────┘
```

---

## 2. Architecture Principles

### 2.1 Core Principles

#### Principle 1: Security by Design
**Statement**: Security controls are integrated at every layer, not bolted on.

**Implications**:
- All data encrypted at rest and in transit
- Principle of least privilege for all service accounts
- Secrets managed in Azure Key Vault with rotation
- Defense-in-depth with multiple security layers
- Continuous security monitoring and alerting

**Evidence**: Security architecture diagram, threat model, control matrix

#### Principle 2: Zero Trust Architecture
**Statement**: Never trust, always verify - authentication and authorization on every request.

**Implications**:
- No implicit trust between services
- Mutual TLS for service-to-service communication
- Token-based authentication with short-lived credentials
- Network micro-segmentation
- Continuous verification of identity and device posture

**Evidence**: ZTA implementation guide, auth flow diagrams

#### Principle 3: Cloud-Native Design
**Statement**: Leverage cloud platform capabilities for scalability and resilience.

**Implications**:
- Containerized microservices on Kubernetes
- Managed services for databases, caching, messaging
- Autoscaling based on demand
- Multi-region deployment for high availability
- Infrastructure as Code (Bicep/Terraform)

**Evidence**: Deployment manifests, IaC templates

#### Principle 4: API-First Development
**Statement**: All functionality exposed via well-documented, versioned APIs.

**Implications**:
- OpenAPI 3.0 specifications for all endpoints
- API versioning strategy (semantic versioning)
- Backward compatibility guarantees
- Comprehensive API documentation
- Contract testing for API stability

**Evidence**: OpenAPI specs, API documentation portal

#### Principle 5: Observability as a Feature
**Statement**: Comprehensive instrumentation for debugging and optimization.

**Implications**:
- Distributed tracing with OpenTelemetry
- Structured logging with correlation IDs
- Metrics collection for performance monitoring
- Real-time dashboards and alerting
- Log aggregation and analysis

**Evidence**: Observability dashboard, alert definitions

#### Principle 6: Fail Fast, Recover Gracefully
**Statement**: Detect failures quickly and maintain system stability.

**Implications**:
- Circuit breakers for external dependencies
- Retry logic with exponential backoff
- Bulkhead isolation to contain failures
- Graceful degradation of non-critical features
- Automated health checks and self-healing

**Evidence**: Resilience patterns implementation, SRE runbooks

---

## 3. Component Architecture

### 3.1 Core Components

#### 3.1.1 Agent Service (Python)

```python
┌─────────────────────────────────────┐
│      Agent Service (Python)         │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │   ChatAgent                   │  │
│  │   - Instructions              │  │
│  │   - Tools                     │  │
│  │   - Memory                    │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   Chat Client (Multi-Provider)│  │
│  │   - Azure OpenAI             │  │
│  │   - OpenAI                   │  │
│  │   - Anthropic                │  │
│  │   - Ollama                   │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   Middleware Pipeline         │  │
│  │   - Auth Middleware           │  │
│  │   - Logging Middleware        │  │
│  │   - Rate Limit Middleware     │  │
│  │   - Validation Middleware     │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Responsibilities**:
- Agent lifecycle management (create, run, terminate)
- Tool execution and function calling
- Conversation state management
- Multi-provider LLM abstraction
- Request/response middleware processing

**Technology Stack**:
- **Runtime**: Python 3.10+ with asyncio
- **Framework**: FastAPI for REST APIs
- **Validation**: Pydantic models
- **Testing**: pytest with asyncio support
- **Packaging**: uv for dependency management

**Interfaces**:
- **REST API**: `/api/v1/agents/{agent_id}/run`
- **gRPC**: `AgentService.Run(RunRequest)`
- **Message Queue**: Agent run requests via Azure Service Bus

**Scaling Strategy**:
- Horizontal pod autoscaling (HPA) on CPU/memory
- Target: 70% CPU utilization
- Min replicas: 2, Max replicas: 20

#### 3.1.2 Agent Service (.NET)

```csharp
┌─────────────────────────────────────┐
│      Agent Service (.NET)           │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │   AIAgent                     │  │
│  │   - Name                      │  │
│  │   - Instructions              │  │
│  │   - Tools                     │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   Response Client             │  │
│  │   - Azure OpenAI              │  │
│  │   - OpenAI                    │  │
│  │   - Azure AI Foundry          │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   Middleware Pipeline         │  │
│  │   - AgentFilterMiddleware     │  │
│  │   - TelemetryMiddleware       │  │
│  │   - ExceptionMiddleware       │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Responsibilities**:
- Enterprise .NET integration scenarios
- High-performance synchronous workloads
- Windows-based deployment support
- Integration with Power Platform

**Technology Stack**:
- **Runtime**: .NET 8.0 LTS
- **Framework**: ASP.NET Core for APIs
- **Testing**: xUnit, NSubstitute, FluentAssertions
- **Packaging**: NuGet packages

**Interfaces**:
- **REST API**: `/api/v1/dotnet-agents/{agent_id}/run`
- **gRPC**: `DotNetAgentService.Run(RunRequest)`
- **In-Process**: Direct C# API invocation

**Scaling Strategy**:
- Kubernetes HPA or Azure App Service scaling
- Target: 70% CPU utilization
- Min replicas: 2, Max replicas: 15

#### 3.1.3 Workflow Engine

```
┌─────────────────────────────────────┐
│         Workflow Engine             │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │   Graph Executor              │  │
│  │   - Node orchestration        │  │
│  │   - Data flow management      │  │
│  │   - Checkpointing             │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   Node Types                  │  │
│  │   - Agent Nodes               │  │
│  │   - Function Nodes            │  │
│  │   - Conditional Nodes         │  │
│  │   - Human-in-Loop Nodes       │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   State Manager               │  │
│  │   - Graph state               │  │
│  │   - Execution history         │  │
│  │   - Time-travel debug         │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Responsibilities**:
- Graph-based workflow execution
- Agent coordination and data passing
- Checkpointing for long-running workflows
- Human-in-the-loop approvals
- Workflow visualization and debugging

**Technology Stack**:
- **Runtime**: Python 3.10+ (primary) / .NET 8.0 (interop)
- **Graph Library**: NetworkX (Python), QuikGraph (.NET)
- **State Store**: Redis for distributed state
- **Serialization**: JSON/MessagePack

**Scaling Strategy**:
- Stateful set with persistent volumes for checkpoints
- Workflow sharding by workflow_id
- Leader election for coordination tasks

#### 3.1.4 DevUI Service

```
┌─────────────────────────────────────┐
│          DevUI Service              │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │   React Frontend              │  │
│  │   - Agent Playground          │  │
│  │   - Workflow Visualizer       │  │
│  │   - Debug Inspector           │  │
│  │   - Trace Timeline            │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   Backend API                 │  │
│  │   - Agent management          │  │
│  │   - Workflow execution        │  │
│  │   - Trace retrieval           │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Responsibilities**:
- Interactive agent development interface
- Real-time workflow visualization
- Debugging tools and trace inspection
- Configuration management UI

**Technology Stack**:
- **Frontend**: React 18, TypeScript, shadcn/ui components
- **Backend**: FastAPI (Python) or ASP.NET Core
- **Communication**: WebSocket for real-time updates
- **Build**: Vite for frontend bundling

---

## 4. Security Architecture

### 4.1 Security Layers

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Perimeter Security                            │
│  - Azure Firewall, DDoS Protection                      │
│  - WAF with OWASP Top 10 protection                     │
│  - API Gateway with rate limiting                       │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Layer 2: Identity & Access Management                  │
│  - Microsoft Entra ID (Azure AD)                        │
│  - OAuth 2.0 + OIDC                                     │
│  - PIV/CAC certificate authentication (federal)         │
│  - RBAC with fine-grained permissions                   │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Layer 3: Application Security                          │
│  - Input validation (Pydantic, FluentValidation)        │
│  - Output encoding                                      │
│  - CSRF protection                                      │
│  - Security headers (CSP, HSTS, X-Frame-Options)        │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Layer 4: Data Security                                 │
│  - TLS 1.3 for data in transit                          │
│  - AES-256-GCM for data at rest                         │
│  - Azure Key Vault for secrets                          │
│  - CUI marking and handling automation                  │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  Layer 5: Infrastructure Security                       │
│  - Network segmentation (VNets, NSGs)                   │
│  - Private endpoints for Azure services                 │
│  - Just-in-time VM access                               │
│  - Azure Policy enforcement                             │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Authentication Flow

```
┌────────┐                  ┌────────────┐                  ┌──────────┐
│ Client │                  │ API Gateway│                  │ Entra ID │
└───┬────┘                  └─────┬──────┘                  └────┬─────┘
    │                             │                              │
    │ 1. Request with JWT         │                              │
    │────────────────────────────>│                              │
    │                             │                              │
    │                             │ 2. Validate token            │
    │                             │─────────────────────────────>│
    │                             │                              │
    │                             │ 3. Token valid + claims      │
    │                             │<─────────────────────────────│
    │                             │                              │
    │                             │ 4. Check RBAC permissions    │
    │                             │ (in API Gateway or service)  │
    │                             │                              │
    │ 5. Forward to service       │                              │
    │<────────────────────────────│                              │
```

### 4.3 Secrets Management

**Principles**:
- No secrets in code or configuration files
- All secrets stored in Azure Key Vault
- Managed identities for service-to-service auth
- Automatic secret rotation (90 days)
- Audit logging for secret access

**Implementation**:
```python
# Python example using Azure SDK
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Uses managed identity in production, Azure CLI in dev
credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://aurelius-kv.vault.azure.net/", credential=credential)

# Retrieve secret
openai_api_key = client.get_secret("openai-api-key").value
```

### 4.4 CUI Handling (Federal)

**Classification Workflow**:
1. **Detection**: Automated scanning for CUI indicators (SSN, FOUO keywords)
2. **Marking**: Automatic banner/footer application to documents
3. **Storage**: Encrypted volumes with access logging
4. **Transmission**: TLS 1.3 with certificate pinning
5. **Disposal**: NIST 800-88 compliant sanitization

**Evidence Trail**:
- All CUI access logged to Azure Sentinel
- Quarterly access reviews
- Annual security awareness training

---

## 5. Data Architecture

### 5.1 Data Flow Diagram

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│   Client    │────────>│  API Gateway │────────>│   Agent    │
│ Application │         │  (Validation)│         │  Service   │
└─────────────┘         └──────────────┘         └─────┬──────┘
                                                        │
                                                        │
                        ┌───────────────────────────────┼───────────────┐
                        │                               │               │
                  ┌─────▼─────┐               ┌─────────▼──────┐  ┌────▼─────┐
                  │    LLM    │               │  State Store   │  │ Context  │
                  │ Providers │               │    (Redis)     │  │ Provider │
                  └───────────┘               └────────────────┘  └──────────┘
                        │
                        │ Response
                        │
                  ┌─────▼─────┐
                  │   Audit   │
                  │    Log    │
                  └───────────┘
```

### 5.2 Data Stores

#### Redis (State Store)
- **Purpose**: Agent conversation state, workflow checkpoints
- **Schema**: Key-value with JSON serialization
- **Retention**: 30 days (configurable)
- **Backup**: Daily snapshots to Azure Blob Storage
- **Encryption**: TLS in transit, AES-256 at rest (Azure Cache for Redis)

#### Mem0 (Context Provider)
- **Purpose**: Long-term agent memory, user preferences
- **Schema**: Vector embeddings + metadata
- **Retention**: User-controlled, GDPR-compliant deletion
- **Backup**: Weekly full backup
- **Encryption**: Client-side encryption before storage

#### Azure Blob Storage (Artifacts)
- **Purpose**: SBOMs, test reports, security scans, logs
- **Schema**: Hierarchical folder structure
- **Retention**: 7 years (federal compliance)
- **Backup**: Geo-redundant storage (GRS)
- **Encryption**: Microsoft-managed keys, AES-256

#### Azure Cosmos DB (Audit Logs)
- **Purpose**: Immutable audit trail for compliance
- **Schema**: JSON documents with partition key on user_id
- **Retention**: 10 years (federal requirement)
- **Backup**: Continuous backup with point-in-time restore
- **Encryption**: Always encrypted, customer-managed keys

### 5.3 Data Lifecycle

```yaml
stages:
  creation:
    - Validate data schema
    - Apply classification labels
    - Encrypt sensitive data
    - Generate audit record

  storage:
    - Store in appropriate tier (hot/cool/archive)
    - Apply retention policy
    - Backup according to schedule
    - Monitor access patterns

  usage:
    - Authenticate and authorize access
    - Log all read/write operations
    - Apply rate limiting
    - Cache for performance

  archival:
    - Move to cool/archive tier after 90 days
    - Maintain encryption
    - Preserve audit trail
    - Enable retrieval if needed

  deletion:
    - Secure deletion per NIST 800-88
    - Delete all copies and backups
    - Update audit log with deletion record
    - Issue deletion certificate (for GDPR)
```

---

## 6. Integration Architecture

### 6.1 Integration Patterns

#### Pattern 1: Synchronous Request-Response
**Use Case**: Real-time agent interactions, simple queries

```
Client ──> API Gateway ──> Agent Service ──> LLM Provider
       <──              <──              <──
```

**Characteristics**:
- Low latency (< 2 seconds P95)
- Timeout after 30 seconds
- Circuit breaker for LLM provider failures

#### Pattern 2: Asynchronous Message Queue
**Use Case**: Long-running workflows, batch processing

```
Client ──> API Gateway ──> Azure Service Bus ──> Workflow Engine
                                                      │
                                                      ▼
                                           State Store (Redis)
```

**Characteristics**:
- Decoupled producer/consumer
- At-least-once delivery guarantee
- Dead letter queue for failures

#### Pattern 3: Event-Driven
**Use Case**: Multi-agent coordination, reactive systems

```
Agent 1 ──> Azure Event Grid ──> Agent 2
                    │
                    ├──> Agent 3
                    │
                    └──> Monitoring Service
```

**Characteristics**:
- Publish-subscribe pattern
- Fan-out to multiple subscribers
- Event schema registry for versioning

### 6.2 External Integrations

#### Microsoft Graph API
```yaml
purpose: Identity, users, groups, calendars, files
authentication: OAuth 2.0 with delegated permissions
rate_limits: 10,000 requests per 10 minutes
retry_strategy: Exponential backoff with jitter
```

#### Azure AI Foundry
```yaml
purpose: Model deployment, fine-tuning, evaluation
authentication: Azure AD managed identity
rate_limits: Based on deployment tier
failover: Multi-region deployment
```

#### Power Platform
```yaml
purpose: Low-code integration, custom connectors
authentication: Service principal
data_flow: REST API with pagination
governance: DLP policies enforced
```

---

## 7. Deployment Architecture

### 7.1 Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Azure Kubernetes Service (AKS)             │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │  Namespace: aurelius-agents-prod                │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  ┌──────────────┐  ┌──────────────┐            │   │
│  │  │ Python Agent │  │  .NET Agent  │            │   │
│  │  │  Deployment  │  │  Deployment  │            │   │
│  │  │   Replicas:3 │  │   Replicas:3 │            │   │
│  │  └──────┬───────┘  └──────┬───────┘            │   │
│  │         │                  │                     │   │
│  │  ┌──────▼──────────────────▼────────┐           │   │
│  │  │      Internal Service            │           │   │
│  │  │   (ClusterIP, Port 8080)         │           │   │
│  │  └──────────────┬───────────────────┘           │   │
│  └─────────────────┼─────────────────────────────┘    │
│                    │                                    │
│  ┌─────────────────▼─────────────────────────────┐    │
│  │         Ingress Controller                     │    │
│  │  (NGINX with TLS termination)                  │    │
│  └─────────────────┬─────────────────────────────┘    │
└────────────────────┼──────────────────────────────────┘
                     │
              ┌──────▼──────┐
              │ Azure Front │
              │    Door     │
              └─────────────┘
```

### 7.2 Infrastructure Components

#### Compute
- **AKS Cluster**: 3 node pools (system, user, spot)
- **Node Size**: Standard_D4s_v5 (4 vCPU, 16 GB RAM)
- **Autoscaling**: Min 3, Max 20 nodes per pool
- **Availability**: 99.95% SLA with multi-zone deployment

#### Networking
- **Virtual Network**: 10.0.0.0/16 CIDR
- **Subnets**: AKS (10.0.1.0/24), AppGW (10.0.2.0/24), PE (10.0.3.0/24)
- **Private Endpoints**: For Key Vault, Storage, Cosmos DB
- **NSG Rules**: Whitelisted IP ranges only

#### Storage
- **Azure Files**: Persistent volumes for workflow state
- **Azure Blob**: Artifact storage (SBOMs, reports)
- **Redis Cache**: Premium tier, 6 GB memory, clustering enabled

### 7.3 Deployment Pipeline

```yaml
stages:
  - stage: Build
    jobs:
      - job: PythonBuild
        steps:
          - Lint and type check
          - Run unit tests
          - Security scanning (Bandit, Semgrep)
          - Build wheel package
          - Generate SBOM

      - job: DotNetBuild
        steps:
          - Restore dependencies
          - Build solution
          - Run unit tests
          - Security scanning (Security Code Scan)
          - Publish artifacts
          - Generate SBOM

  - stage: Test
    jobs:
      - Integration tests
      - Performance tests
      - Security tests (OWASP ZAP)

  - stage: Deploy_Dev
    environment: Development
    steps:
      - Apply Kubernetes manifests
      - Run smoke tests
      - Verify health endpoints

  - stage: Deploy_Staging
    environment: Staging
    steps:
      - Blue-green deployment
      - Run full regression suite
      - Load testing
      - Manual approval gate

  - stage: Deploy_Prod
    environment: Production
    steps:
      - Canary deployment (10% traffic)
      - Monitor error rates and latency
      - Gradual rollout to 100%
      - Automated rollback on failure
```

---

## 8. Observability Architecture

### 8.1 Observability Pillars

```
┌──────────────────────────────────────────────────┐
│              Application Code                     │
│  (Instrumented with OpenTelemetry SDK)           │
└────────────┬──────────────┬──────────────────────┘
             │              │
      ┌──────▼────┐  ┌──────▼────┐  ┌──────────┐
      │  Traces   │  │   Logs    │  │ Metrics  │
      └──────┬────┘  └──────┬────┘  └─────┬────┘
             │              │              │
             └──────┬───────┴──────┬───────┘
                    │              │
         ┌──────────▼──────────────▼─────────┐
         │  OpenTelemetry Collector          │
         │  (Aggregation, Filtering, Export) │
         └──────────┬───────────────┬─────────┘
                    │               │
         ┌──────────▼────────┐  ┌──▼──────────────┐
         │  Azure Monitor    │  │ Grafana Cloud   │
         │  Application      │  │ (Dashboards &   │
         │  Insights         │  │  Alerting)      │
         └───────────────────┘  └─────────────────┘
```

### 8.2 Tracing Strategy

**Span Structure**:
```yaml
span_name: agent.run
attributes:
  agent.id: "agent-123"
  agent.name: "CustomerSupportBot"
  agent.provider: "azure-openai"
  agent.model: "gpt-4o"
  user.id: "user-456"
  session.id: "session-789"
events:
  - name: "tool.call"
    attributes:
      tool.name: "get_weather"
      tool.input: '{"location": "Seattle"}'
  - name: "tool.result"
    attributes:
      tool.output: '{"temp": 65, "condition": "sunny"}'
```

**Trace Propagation**:
- W3C Trace Context standard
- Baggage for cross-service metadata
- Correlation ID in all log messages

### 8.3 Metrics Collection

**Golden Signals**:
```yaml
latency:
  - agent_run_duration_seconds (histogram)
  - llm_request_duration_seconds (histogram)
  - workflow_execution_duration_seconds (histogram)

traffic:
  - agent_runs_total (counter)
  - api_requests_total (counter)
  - workflow_executions_total (counter)

errors:
  - agent_errors_total (counter)
  - llm_errors_total (counter)
  - workflow_failures_total (counter)

saturation:
  - agent_concurrent_runs (gauge)
  - redis_memory_usage_bytes (gauge)
  - kubernetes_pod_cpu_usage (gauge)
```

**Custom Metrics**:
```yaml
business_metrics:
  - agent_tool_calls_total (counter by tool_name)
  - agent_tokens_consumed_total (counter)
  - agent_cost_usd_total (counter)
  - workflow_nodes_executed_total (counter)
```

### 8.4 Alerting Rules

**Critical Alerts** (PagerDuty escalation):
```yaml
- name: HighErrorRate
  condition: error_rate > 5% for 5 minutes
  severity: critical

- name: ServiceDown
  condition: health_check failing for 2 minutes
  severity: critical

- name: SecurityIncident
  condition: unauthorized_access_attempts > 10 in 1 minute
  severity: critical
```

**Warning Alerts** (Slack notification):
```yaml
- name: ElevatedLatency
  condition: p95_latency > 3 seconds for 10 minutes
  severity: warning

- name: HighMemoryUsage
  condition: memory_usage > 85% for 15 minutes
  severity: warning
```

---

## 9. Architecture Decision Records (ADRs)

### ADR-001: Use Python and .NET for Multi-Language Support
**Status**: Accepted
**Context**: Customers have diverse technology stacks
**Decision**: Support both Python and .NET with feature parity
**Consequences**: Increased maintenance, but broader market reach

### ADR-002: Redis for State Management
**Status**: Accepted
**Context**: Need distributed state for agent conversations
**Decision**: Use Azure Cache for Redis with persistence
**Consequences**: Scalable, but adds external dependency

### ADR-003: OpenTelemetry for Observability
**Status**: Accepted
**Context**: Need vendor-neutral observability solution
**Decision**: Use OpenTelemetry SDK and Collector
**Consequences**: Future-proof, multi-backend support

### ADR-004: Kubernetes for Container Orchestration
**Status**: Accepted
**Context**: Need scalable, resilient deployment platform
**Decision**: Use Azure Kubernetes Service (AKS)
**Consequences**: Operational complexity, but industry standard

### ADR-005: Azure Key Vault for Secrets Management
**Status**: Accepted
**Context**: Need secure, auditable secrets storage
**Decision**: Use Azure Key Vault with managed identities
**Consequences**: Azure lock-in, but FIPS 140-2 Level 2 compliant

---

## 10. Future Architecture Considerations

### 10.1 Edge Deployment
**Goal**: Run agents on-premises or in disconnected environments
**Approach**: Containerized edge runtime with local LLM (Ollama)
**Timeline**: Q3 2025

### 10.2 Multi-Cloud Support
**Goal**: Deploy on AWS, GCP, or hybrid scenarios
**Approach**: Abstract cloud services behind interfaces
**Timeline**: Q4 2025

### 10.3 Advanced Orchestration
**Goal**: Complex multi-agent workflows with conditional logic
**Approach**: Workflow DSL or visual designer
**Timeline**: Q2 2025

---

## Appendices

### A. Technology Radar
**Adopt**: Azure OpenAI, Kubernetes, OpenTelemetry, FastAPI
**Trial**: Anthropic Claude, Ollama, Mem0, uv package manager
**Assess**: Azure AI Foundry Agent Service, Langfuse, DSPy
**Hold**: Legacy Python 3.9, pip-tools, custom tracing

### B. Reference Architecture Diagrams
All detailed diagrams available in `.aurelius/diagrams/` folder.

---

**Document Control**
Last Updated: 2025-10-13
Next Review: 2025-11-13
Owner: Aurelius Technical Architecture Team
