from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class ProposalAgent(BaseAgent):
    def __init__(self):
        super().__init__("Proposal Agent", "Creates final AI use case proposals")

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        company_info = inputs.get("company_info", {})
        industry_info = inputs.get("industry_info", {})
        use_cases = inputs.get("use_cases", [])
        ai_standards = inputs.get("ai_standards", {})
        resources = inputs.get("resources", [])
        industry = inputs.get("industry", "")
        company_name = inputs.get("company_name", "")

        self.log_info("Creating final proposal")

        # Rank and filter use cases
        top_use_cases = self._rank_use_cases(use_cases, company_info)

        # Create comprehensive proposal
        proposal = self._create_proposal(
            company_name, industry, company_info, industry_info,
            top_use_cases, ai_standards, resources
        )

        # Save proposal to file
        self._save_proposal(proposal)

        return {
            "proposal": proposal,
            "top_use_cases": top_use_cases
        }

    def _rank_use_cases(self, use_cases: List[Dict], company_info: Dict) -> List[Dict]:
        """Rank use cases by relevance and impact"""

        # Simple ranking based on impact and feasibility
        for use_case in use_cases:
            score = 0
            
            # Score based on category relevance
            if use_case.get("category") == "Customer Experience":
                score += 3
            elif use_case.get("category") == "Operations":
                score += 2
            else:
                score += 1

            # Score based on technology maturity
            tech = use_case.get("technology", "").lower()
            if "ml" in tech or "machine learning" in tech:
                score += 2
            if "ai" in tech or "llm" in tech:
                score += 1
            
            use_case["score"] = score
        
        # Sort by score and return top 5
        ranked = sorted(use_cases, key=lambda x: x.get("score", 0), reverse=True)
        return ranked[:5]

    def _create_proposal(self, company_name: str, industry: str, company_info: Dict,
                        industry_info: Dict, use_cases: List[Dict], 
                        ai_standards: Dict, resources: List[Dict]) -> Dict:
        """Create comprehensive proposal document"""
        
        proposal = {
            "executive_summary": {
                "company": company_name,
                "industry": industry,
                "overview": company_info.get("overview", ""),
                "ai_opportunity": f"Based on our analysis, {company_name} can leverage AI/ML technologies to improve operations, enhance customer experience, and drive innovation in the {industry} sector."
            },
            "market_analysis": {
                "industry_trends": industry_info.get("trends", []),
                "challenges": industry_info.get("challenges", []),
                "ai_adoption": ai_standards.get("ai_adoption_trends", []),
                "market_leaders": ai_standards.get("industry_leaders", [])
            },
            "recommended_use_cases": use_cases,
            "implementation_roadmap": self._create_roadmap(use_cases),
            "resource_requirements": {
                "datasets": [r for r in resources if r.get("type") == "Dataset"],
                "models": [r for r in resources if "Model" in r.get("type", "")],
                "code_repositories": [r for r in resources if r.get("type") == "Code Repository"]
            },
            "expected_benefits": self._calculate_benefits(use_cases),
            "next_steps": [
                "Conduct detailed feasibility analysis for top 3 use cases",
                "Prepare proof-of-concept for highest priority use case",
                "Establish AI/ML team and infrastructure",
                "Begin data collection and preparation"
            ]
        }
        
        return proposal

    def _create_roadmap(self, use_cases: List[Dict]) -> List[Dict]:
        """Create implementation roadmap"""
        
        roadmap = []
        for i, use_case in enumerate(use_cases[:3]):  # Top 3 use cases
            phase = {
                "phase": f"Phase {i+1}",
                "duration": "3-6 months" if i == 0 else "6-9 months",
                "use_case": use_case["title"],
                "key_activities": [
                    "Data collection and preparation",
                    "Model development and training",
                    "Testing and validation",
                    "Deployment and monitoring"
                ]
            }
            roadmap.append(phase)
            
        return roadmap

    def _calculate_benefits(self, use_cases: List[Dict]) -> Dict:
        """Calculate expected benefits"""
        
        return {
            "operational_efficiency": "15-25% improvement in process efficiency",
            "cost_reduction": "10-20% reduction in operational costs",
            "customer_satisfaction": "20-30% improvement in customer experience metrics",
            "competitive_advantage": "First-mover advantage in AI adoption within industry segment"
        }

    def _save_proposal(self, proposal: Dict):
        """Save proposal to JSON and Markdown files"""
        
        # Save as JSON
        with open("outputs/proposal.json", "w") as f:
            json.dump(proposal, f, indent=2)
            
        # Save as Markdown
        self._create_markdown_report(proposal)
            
        self.log_info("Proposal saved to outputs/proposal.json and outputs/proposal.md")

    def _create_markdown_report(self, proposal: Dict):
        """Create a formatted markdown report"""
        
        md_content = f"""# AI/ML Use Case Proposal for {proposal['executive_summary']['company']}

## Executive Summary
**Company**: {proposal['executive_summary']['company']}
**Industry**: {proposal['executive_summary']['industry']}

{proposal['executive_summary']['ai_opportunity']}

## Market Analysis
### Industry Trends
"""
        for trend in proposal['market_analysis']['industry_trends']:
            md_content += f"- {trend}\n"
            
        md_content += "\n### AI Adoption Trends\n"
        for trend in proposal['market_analysis']['ai_adoption']:
            md_content += f"- {trend}\n"
            
        md_content += "\n## Recommended Use Cases\n\n"
        
        for i, use_case in enumerate(proposal['recommended_use_cases'], 1):
            md_content += f"""### {i}. {use_case['title']}
**Description**: {use_case['description']}
**Category**: {use_case['category']}
**Technology**: {use_case['technology']}
**Expected Impact**: {use_case['impact']}

"""
            
        md_content += "## Implementation Roadmap\n\n"
        for phase in proposal['implementation_roadmap']:
            md_content += f"""### {phase['phase']} - {phase['use_case']}
**Duration**: {phase['duration']}
**Key Activities**:
"""
            for activity in phase['key_activities']:
                md_content += f"- {activity}\n"
            md_content += "\n"
            
        md_content += """## Expected Benefits
- **Operational Efficiency**: 15-25% improvement in process efficiency
- **Cost Reduction**: 10-20% reduction in operational costs
- **Customer Satisfaction**: 20-30% improvement in customer experience metrics
- **Competitive Advantage**: First-mover advantage in AI adoption

## Next Steps
1. Conduct detailed feasibility analysis for top 3 use cases
2. Prepare proof-of-concept for highest priority use case
3. Establish AI/ML team and infrastructure
4. Begin data collection and preparation
"""
        
        with open("outputs/proposal.md", "w") as f:
            f.write(md_content)