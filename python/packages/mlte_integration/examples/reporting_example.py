"""
Example: Using ReportingAgent to generate comprehensive evaluation reports.

Federal Compliance: SA-11, SI-5
"""

import asyncio
from pathlib import Path
from mlte_integration.agents.reporting import ReportingAgent, ReportFormat


async def main():
    """Demonstrate ReportingAgent usage."""

    # Sample evaluation results (from all previous agents)
    evaluation_results = {
        "negotiation_card": {"name": "Security Agent", "category": "CUI"},
        "validation_results": {
            "overall_status": "FAIL",
            "gate_results": [
                {
                    "name": "Prompt Injection Resistance",
                    "status": "FAIL",
                    "severity": "blocking",
                    "measured_value": 0.89,
                    "expected_value": 0.95,
                    "reasoning": "Below threshold by 6%",
                },
                {
                    "name": "PII Protection",
                    "status": "PASS",
                    "severity": "blocking",
                    "measured_value": 0.005,
                    "expected_value": 0.01,
                },
                {
                    "name": "Performance SLA",
                    "status": "PASS",
                    "severity": "warning",
                    "measured_value": 1500,
                    "expected_value": 2000,
                },
            ],
        },
        "qas_results": [
            {
                "name": "Prompt Injection Test",
                "measurement": "0.89 success rate",
                "threshold": ">= 0.95",
                "status": "FAIL",
            },
        ],
        "compliance_mappings": {
            "nist_ai_rmf": {
                "Valid and Reliable": "PASS",
                "Safe": "WARNING",
                "Secure and Resilient": "FAIL",
                "Accountable and Transparent": "PASS",
            },
        },
    }

    print("\n" + "="*80)
    print("MLTE ReportingAgent - Comprehensive Report Generation")
    print("="*80)

    # Initialize ReportingAgent
    output_dir = Path("mlte_reports")
    agent = ReportingAgent(
        output_dir=output_dir,
        formats=[ReportFormat.MARKDOWN, ReportFormat.JSON, ReportFormat.HTML],
    )

    print(f"\n📝 Generating reports in {len(agent.formats)} formats...")
    print(f"   Output directory: {output_dir}")

    # Generate reports
    results = await agent.generate_reports(
        evaluation_results,
        agent_spec={"name": "SecurityAgent", "version": "1.0.0"},
    )

    # Display results
    print("\n✅ Report generation complete!")
    print(f"\n📊 Reports generated: {len(results['reports'])}")
    for report_path in results["reports"]:
        print(f"   - {report_path}")

    if results["dashboards"]:
        print(f"\n📈 Dashboards generated: {len(results['dashboards'])}")
        for dashboard_path in results["dashboards"]:
            print(f"   - {dashboard_path}")

    # Show sample report content
    if results["reports"]:
        md_report = next((r for r in results["reports"] if r.suffix == ".md"), None)
        if md_report:
            print("\n" + "-"*80)
            print("SAMPLE REPORT CONTENT (Markdown)")
            print("-"*80)
            print(md_report.read_text()[:500] + "\n...")

    print("\n" + "="*80)
    print("📋 Federal Compliance:")
    print("   - SA-11: Developer Security Testing and Evaluation")
    print("   - SI-5: Security Alerts, Advisories, and Directives")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
