"""
Federal compliance report generation example.

This sample demonstrates generating comprehensive federal
compliance reports including NIST AI RMF and CMMC mappings.

Usage:
    python samples/federal_compliance_report.py

Federal Compliance:
- NIST AI RMF mapping
- CMMC L2 control coverage
- OSCAL document generation
"""

import asyncio
import json

from agent_framework_mlte_integration.config import MLTEConfig
from agent_framework_mlte_integration.types import CMMC_LEVEL_2_DOMAINS, NIST_AI_RMF_CHARACTERISTICS


async def main():
    """Generate federal compliance report."""
    print("=" * 60)
    print("Federal Compliance Report Example")
    print("=" * 60)

    # Load MLTE configuration
    config = MLTEConfig.load()

    print("\nFederal Compliance Configuration:")
    print(f"  Enabled: {config.federal_compliance.enabled}")
    print(f"  Standards: {', '.join(config.federal_compliance.standards)}")
    print(f"  OSCAL Export: {config.federal_compliance.oscal_export}")
    print(f"  Classification: {config.federal_compliance.classification}")

    print("\nNIST AI RMF Characteristics:")
    for i, characteristic in enumerate(NIST_AI_RMF_CHARACTERISTICS, 1):
        print(f"  {i}. {characteristic}")

    print("\nCMMC Level 2 Domains:")
    for i, domain in enumerate(CMMC_LEVEL_2_DOMAINS, 1):
        print(f"  {i}. {domain}")

    print("\nGenerating compliance report...")
    print("(Implementation pending)")

    # TODO: Generate actual compliance report
    # compliance_agent = FederalComplianceAgent(chat_client=chat_client)
    # compliance_report = await compliance_agent.run(report_id="example_report")
    #
    # print("\nCompliance Report Generated:")
    # print(f"  NIST AI RMF Coverage: {compliance_report.nist_ai_rmf_coverage:.1%}")
    # print(f"  CMMC Coverage: {compliance_report.cmmc_coverage:.1%}")
    # print(f"  Gaps Identified: {len(compliance_report.gaps)}")
    #
    # if compliance_report.oscal_document:
    #     print("\nOSCAL Document:")
    #     print(json.dumps(compliance_report.oscal_document, indent=2))

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
