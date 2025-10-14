# Aurelius Microsoft Agent Framework
## Federally-Compliant AI Agent Platform

[![CMMC Level 2](https://img.shields.io/badge/CMMC-Level%202-green)](https://www.acq.osd.mil/cmmc/)
[![NIST 800-171](https://img.shields.io/badge/NIST-800--171-blue)](https://csrc.nist.gov/publications/detail/sp/800-171/rev-2/final)
[![SDVOSB](https://img.shields.io/badge/SDVOSB-Certified-red)](https://www.va.gov/osdbu/verification/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Mission

Deliver a production-ready, federally-compliant implementation of Microsoft Agent Framework that enables Aurelius Tech & Talent Solutions to build secure, scalable AI agent solutions for government and commercial clients.

## 🏆 Key Differentiators

- **Federal Ready**: CMMC L2, NIST 800-171, FedRAMP Moderate compliance built-in
- **Security First**: Zero-trust architecture, automated security scanning, PIV/CAC authentication
- **Evidence-Based**: Complete audit trail with SBOM, security scans, test coverage
- **Multi-Platform**: Full Python 3.10+ and .NET 8.0+ support with feature parity
- **Enterprise Grade**: Production-tested patterns, observability, disaster recovery

## 📋 Quick Links

- **[Original Microsoft Docs](README.md)** - Upstream Microsoft Agent Framework documentation
- **[Aurelius PRD](.aurelius/PRD.md)** - Product requirements and acceptance criteria
- **[Architecture Doc](.aurelius/ARCHITECTURE.md)** - Technical architecture and design decisions
- **[Security Controls](.aurelius/security/security-controls.yaml)** - CMMC/NIST control mapping
- **[Project CLAUDE.md](.aurelius/CLAUDE.md)** - Development standards and workflows

## 🚀 Getting Started

### Prerequisites

**For Python Development:**
- Python 3.10, 3.11, 3.12, or 3.13
- Git with GPG signing configured
- Azure CLI (for authentication in dev)
- Access to Aurelius Azure tenant

**For .NET Development:**
- .NET 8.0 SDK or later
- Visual Studio 2022+ or VS Code
- Azure CLI (for authentication in dev)

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/AureliustechandTalentSolutions/Microsoft-agent-framework.git
cd Microsoft-agent-framework
```

#### 2. Setup Python Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install uv package manager
pip install uv

# Install all dependencies including dev/security/compliance
uv pip install -e .[all]

# Setup pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

#### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# For local dev, you can use Azure CLI authentication:
az login --tenant 944b3898-fcbe-4631-91e1-794e102c9c7d
```

#### 4. Verify Installation

```bash
# Run tests
pytest --cov --cov-report=html

# Run security scans
bandit -r . && semgrep --config=auto

# Check types
mypy . && pyright .

# Format code
ruff check --fix . && black . && isort .
```

## 🔐 Security & Compliance

### Security Standards

- **CMMC Level 2**: All 110 practices implemented and documented
- **NIST 800-171**: Rev 2 compliance with evidence artifacts
- **FedRAMP**: Moderate baseline controls (in progress)
- **SSDF**: Secure Software Development Framework practices

### Security Features

- ✅ Zero-trust architecture with defense-in-depth
- ✅ PIV/CAC certificate authentication for federal users
- ✅ TLS 1.3 with FIPS 140-2 approved ciphers
- ✅ AES-256-GCM encryption at rest
- ✅ Azure Key Vault secrets management
- ✅ Automated CUI marking and handling
- ✅ Comprehensive audit logging to immutable storage
- ✅ Daily vulnerability scanning with 24-hour remediation SLA

### Evidence Artifacts

All compliance evidence stored in [`.aurelius/evidence/`](.aurelius/evidence/):
- **SBOM**: Software Bill of Materials (CycloneDX format)
- **Security**: Bandit, Semgrep, Safety, pip-audit results
- **Testing**: Coverage reports, mutation testing scores
- **Compliance**: License reports, control attestations
- **Audit**: Access logs, security events (10-year retention)

## 🏗️ Architecture

### High-Level Components

```
┌─────────────────────────────────────────┐
│         Client Applications             │
│   (Web, Mobile, CLI, Power Platform)   │
└──────────────┬──────────────────────────┘
               │ HTTPS/gRPC
┌──────────────▼──────────────────────────┐
│         API Gateway (Azure APIM)        │
│   Auth, Rate Limiting, Routing          │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼────┐ ┌──▼─────┐ ┌──▼────────┐
│ Python │ │ .NET   │ │ Workflow  │
│ Agents │ │ Agents │ │ Engine    │
└───┬────┘ └──┬─────┘ └──┬────────┘
    │         │          │
    └─────────┼──────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼────┐ ┌─▼──────┐ ┌▼────────┐
│  LLM   │ │ State  │ │ Context │
│Provider│ │(Redis) │ │ (Mem0)  │
└────────┘ └────────┘ └─────────┘
```

### Key Technologies

**Backend:**
- Python 3.10+ with asyncio, FastAPI
- .NET 8.0 with ASP.NET Core
- Azure OpenAI, OpenAI, Anthropic, Ollama

**Infrastructure:**
- Azure Kubernetes Service (AKS)
- Azure Cache for Redis (state)
- Azure Cosmos DB (audit logs)
- Azure Key Vault (secrets)
- Azure Monitor + OpenTelemetry (observability)

**Security:**
- Microsoft Entra ID (authentication)
- Azure API Management (gateway)
- Azure Sentinel (SIEM)
- Azure Security Center (compliance)

## 📚 Development Workflow

### DSPy Role-Based Development

We use a structured DSPy pipeline for evidence-based development:

```
PLANNER → DECOMPOSER → EXECUTOR → REVIEWER → TESTER → MERGER
```

Each role generates specific evidence artifacts and enforces quality gates.

### Git Workflow

**Branches:**
- `main`: Production-ready, requires 2 approvals + all gates
- `develop`: Integration branch, requires 1 approval
- `feature/AF-{ID}-description`: Feature branches
- `security/CVE-{ID}`: Security patches
- `compliance/CMMC-{control}`: Compliance implementations

**Commit Format:**
```
type(scope): description [evidence: path]

Types: feat, fix, docs, test, security, compliance, refactor
Scope: python, dotnet, workflows, agents, mcp, devui
Evidence: Path to artifacts generated
```

### Quality Gates

**Pre-Commit (Automated):**
- ✅ Linting (Ruff, Black, isort)
- ✅ Type checking (MyPy strict, Pyright)
- ✅ Security (Bandit, detect-secrets)
- ✅ Unit tests pass

**Pre-Merge (CI Pipeline):**
- ✅ All tests pass (85%+ coverage)
- ✅ Mutation testing (65%+ score)
- ✅ Security scans (zero critical vulnerabilities)
- ✅ SBOM and license compliance
- ✅ Code review (2 approvals)

**Pre-Release:**
- ✅ Staging deployment success
- ✅ Performance benchmarks met
- ✅ Security authorization artifacts (federal)

## 🧪 Testing

### Test Categories

```bash
# Unit tests
pytest -m unit

# Integration tests
pytest -m integration

# Security tests
pytest -m security

# Compliance tests
pytest -m compliance

# All tests with coverage
pytest --cov --cov-report=html --cov-fail-under=85
```

### Mutation Testing

```bash
# Run mutation testing
mutmut run

# View results
mutmut results

# Generate HTML report
mutmut html
```

## 🔍 Observability

### OpenTelemetry Integration

All agents are instrumented with OpenTelemetry for:
- **Distributed Tracing**: Full request flow visibility
- **Metrics**: Latency, throughput, error rates
- **Logs**: Structured logging with correlation IDs

### Monitoring Dashboards

- **Azure Monitor**: Production monitoring and alerting
- **Grafana Cloud**: Real-time metrics and visualization
- **Azure Sentinel**: Security event correlation

## 📦 Deployment

### Environments

1. **Development**: Local development, Azure CLI auth
2. **Staging**: Pre-production validation, full security controls
3. **Production (Commercial)**: SOC 2 Type II compliant
4. **Production (Federal)**: CMMC L2, FedRAMP Moderate, IL4/IL5 ready

### Deployment Methods

- **Azure Kubernetes Service**: Containerized microservices
- **Azure App Service**: Simplified .NET hosting
- **Azure Functions**: Serverless agent execution

## 🤝 Contributing

We follow strict contribution guidelines to maintain federal compliance:

1. **Fork and Branch**: Create feature branch from `develop`
2. **Sign Commits**: All commits must be GPG signed
3. **Quality Gates**: Pass all pre-commit and CI checks
4. **Documentation**: Update docs and ADRs for architectural changes
5. **Security Review**: Required for authentication, encryption, or data handling changes
6. **Evidence**: Generate and commit all evidence artifacts

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🏢 Organization

**Aurelius Tech & Talent Solutions**
- **SDVOSB**: Service-Disabled Veteran-Owned Small Business
- **MBE**: Minority Business Enterprise
- **Microsoft Partner**: AI Cloud Partner

## 📞 Contact

- **Technical Support**: support@aureliustech.com
- **Security Issues**: security@aureliustech.com
- **Compliance Questions**: compliance@aureliustech.com
- **Sales Inquiries**: sales@aureliustech.com

## 🔗 Resources

### Aurelius Resources
- [Aurelius Federal Platform](https://github.com/AureliustechandTalentSolutions/Resource-libraryAurelius-Federal-Platform)
- [Federal Proposal Templates](https://github.com/AureliustechandTalentSolutions/Resource-libraryAurelius-Federal-Platform/tree/main/templates)
- [CMMC Compliance Guide](https://github.com/AureliustechandTalentSolutions/Resource-libraryAurelius-Federal-Platform/tree/main/compliance)

### Microsoft Resources
- [Agent Framework Docs](https://learn.microsoft.com/agent-framework/)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [Azure AI Foundry](https://azure.microsoft.com/en-us/products/ai-studio/)

### Compliance Resources
- [CMMC v2.0](https://www.acq.osd.mil/cmmc/)
- [NIST 800-171](https://csrc.nist.gov/publications/detail/sp/800-171/rev-2/final)
- [FedRAMP](https://www.fedramp.gov/)
- [SSDF (SP 800-218)](https://csrc.nist.gov/publications/detail/sp/800-218/final)

---

**🛡️ This implementation is designed for federal government use and maintains the highest standards of security and compliance.**

Last Updated: 2025-10-13 | Version: 1.0.0
