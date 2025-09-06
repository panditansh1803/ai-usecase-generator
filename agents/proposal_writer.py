import json
from datetime import datetime

class ProposalWriter:
    def write_proposal(self, company_data, industry_data, use_cases, resources):
        """Generate comprehensive proposal"""
        print("📝 Writing proposal...")
        
        proposal_data = {
            "executive_summary": {
                "company": company_data['company_name'],
                "industry": company_data['industry'],
                "overview": company_data['company_info']['overview'][:300] + '...',
                "ai_opportunity": f"Based on our analysis, {company_data['company_name']} can leverage AI/ML technologies to improve operations, enhance customer experience, and drive innovation in the {company_data['industry']} sector."
            },
            
            "market_analysis": {
                "industry_trends": industry_data['trends'],
                "challenges": industry_data['challenges'],
                "ai_adoption": [
                    "Growing adoption of AI across industry",
                    "Focus on automation and efficiency",
                    "Investment in digital transformation"
                ]
            },
            
            "recommended_use_cases": use_cases,
            
            "implementation_roadmap": self._create_roadmap(use_cases),
            
            "resource_requirements": {
                "datasets": [],
                "models": [r for r in resources if r.get('source') == 'HuggingFace'],
                "code_repositories": [r for r in resources if r.get('source') == 'GitHub']
            },
            
            "expected_benefits": {
                "operational_efficiency": "15-25% improvement in process efficiency",
                "cost_reduction": "10-20% reduction in operational costs",
                "customer_satisfaction": "20-30% improvement in customer experience metrics",
                "competitive_advantage": f"First-mover advantage in AI adoption within {company_data['industry']} segment"
            },
            
            "next_steps": [
                "Conduct detailed feasibility analysis for top 3 use cases",
                "Prepare proof-of-concept for highest priority use case",
                "Establish AI/ML team and infrastructure",
                "Begin data collection and preparation"
            ]
        }
        
        # Generate markdown version
        markdown_proposal = self._generate_markdown(proposal_data)
        
        return proposal_data, markdown_proposal
    
    def _create_roadmap(self, use_cases):
        """Create implementation roadmap"""
        roadmap = []
        durations = ["3-6 months", "6-9 months", "9-12 months"]
        
        for i, use_case in enumerate(use_cases[:3]):
            roadmap.append({
                "phase": f"Phase {i+1}",
                "duration": durations[i],
                "use_case": use_case['title'],
                "key_activities": [
                    "Data collection and preparation",
                    "Model development and training",
                    "Testing and validation",
                    "Deployment and monitoring"
                ]
            })
        
        return roadmap
    
    def _generate_markdown(self, data):
        """Generate markdown proposal"""
        markdown = f"""# AI/ML Use Case Proposal for {data['executive_summary']['company']}

## Executive Summary
**Company**: {data['executive_summary']['company']}
**Industry**: {data['executive_summary']['industry']}

{data['executive_summary']['ai_opportunity']}

## Market Analysis
### Industry Trends
"""
        for trend in data['market_analysis']['industry_trends']:
            markdown += f"- {trend}\n"
        
        markdown += "\n### AI Adoption Trends\n"
        for adoption in data['market_analysis']['ai_adoption']:
            markdown += f"- {adoption}\n"
        
        markdown += "\n## Recommended Use Cases\n"
        for i, use_case in enumerate(data['recommended_use_cases'], 1):
            markdown += f"""
### {i}. {use_case['title']}
**Description**: {use_case['description']}
**Category**: {use_case['category']}
**Technology**: {use_case['technology']}
**Expected Impact**: {use_case['impact']}
"""
        
        return markdown
