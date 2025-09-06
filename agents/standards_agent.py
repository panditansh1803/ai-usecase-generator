import requests
import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class StandardsAgent:
    """Agent responsible for analyzing industry standards and generating AI use cases"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com/search"
        
        # Pre-defined use case templates by industry
        self.use_case_templates = {
            'technology': [
                'Automated Code Review and Quality Assurance',
                'Intelligent Customer Support Chatbots',
                'Predictive System Maintenance',
                'AI-Powered Development Tools',
                'Automated Testing and QA'
            ],
            'automotive': [
                'Predictive Maintenance for Manufacturing Equipment',
                'Quality Control with Computer Vision',
                'Supply Chain Optimization',
                'Autonomous Vehicle Development',
                'Customer Experience Personalization'
            ],
            'healthcare': [
                'Medical Image Analysis and Diagnostics',
                'Electronic Health Record Analysis',
                'Drug Discovery and Development',
                'Patient Risk Prediction',
                'Clinical Decision Support Systems'
            ],
            'finance': [
                'Fraud Detection and Prevention',
                'Algorithmic Trading Systems',
                'Credit Risk Assessment',
                'Customer Service Automation',
                'Regulatory Compliance Monitoring'
            ],
            'retail': [
                'Personalized Product Recommendations',
                'Inventory Management Optimization',
                'Customer Behavior Analytics',
                'Dynamic Pricing Strategies',
                'Supply Chain Forecasting'
            ],
            'manufacturing': [
                'Predictive Equipment Maintenance',
                'Quality Control Automation',
                'Production Planning Optimization',
                'Supply Chain Risk Management',
                'Worker Safety Monitoring'
            ]
        }
        
    def execute(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute standards analysis and use case generation"""
        try:
            company_info = research_data.get('company_info', {})
            industry_info = research_data.get('industry_info', {})
            
            company_name = company_info.get('name', '')
            industry = company_info.get('industry', '').lower()
            
            logger.info(f"🎯 Generating AI use cases for {company_name} in {industry}")
            
            # Analyze industry standards
            standards = self._analyze_industry_standards(industry)
            
            # Generate specific use cases
            use_cases = self._generate_use_cases(company_info, industry_info, standards)
            
            # Categorize use cases
            categorized_cases = self._categorize_use_cases(use_cases)
            
            # Assess feasibility and impact
            assessed_cases = self._assess_use_cases(categorized_cases, company_info)
            
            results = {
                'industry_standards': standards,
                'use_cases': assessed_cases,
                'use_case_summary': self._create_use_case_summary(assessed_cases),
                'implementation_priorities': self._prioritize_use_cases(assessed_cases)
            }
            
            logger.info(f"✅ Generated {len(assessed_cases)} use cases for {company_name}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Standards analysis failed: {str(e)}")
            return self._create_fallback_use_cases(research_data)
    
    def _analyze_industry_standards(self, industry: str) -> Dict[str, Any]:
        """Analyze industry standards and AI adoption patterns"""
        try:
            # Search for industry AI standards and best practices
            query = f"{industry} industry AI standards best practices 2024"
            search_results = self._perform_search(query)
            
            standards = {
                'industry': industry,
                'ai_maturity': 'Medium',
                'common_applications': [],
                'regulatory_requirements': [],
                'technology_trends': []
            }
            
            if search_results:
                all_content = ' '.join([result.get('content', '') for result in search_results])
                
                # Extract common AI applications
                ai_applications = [
                    'machine learning', 'natural language processing', 'computer vision',
                    'predictive analytics', 'automation', 'chatbots', 'recommendation systems'
                ]
                
                for app in ai_applications:
                    if app in all_content.lower():
                        standards['common_applications'].append(app.title())
                
                # Extract technology trends
                tech_trends = [
                    'cloud computing', 'edge computing', 'IoT integration',
                    'real-time analytics', 'deep learning', 'generative AI'
                ]
                
                for trend in tech_trends:
                    if trend in all_content.lower():
                        standards['technology_trends'].append(trend.title())
            
            return standards
            
        except Exception as e:
            logger.warning(f"⚠️ Standards analysis failed: {str(e)}")
            return {
                'industry': industry,
                'ai_maturity': 'Medium',
                'common_applications': ['Machine Learning', 'Automation'],
                'technology_trends': ['Cloud Computing', 'Analytics']
            }
    
    def _generate_use_cases(self, company_info: Dict, industry_info: Dict, standards: Dict) -> List[Dict]:
        """Generate specific AI use cases for the company"""
        try:
            industry = company_info.get('industry', '').lower()
            company_name = company_info.get('name', '')
            
            use_cases = []
            
            # Get base use cases for the industry
            base_cases = self.use_case_templates.get(industry, self.use_case_templates['technology'])
            
            # Generate specific use cases
            for i, base_case in enumerate(base_cases):
                use_case = {
                    'id': f"UC_{i+1:02d}",
                    'title': base_case,
                    'description': self._generate_use_case_description(base_case, company_info),
                    'category': self._determine_category(base_case),
                    'technology': self._determine_technology_stack(base_case),
                    'business_value': self._assess_business_value(base_case, company_info),
                    'implementation_complexity': self._assess_complexity(base_case),
                    'timeline': self._estimate_timeline(base_case)
                }
                use_cases.append(use_case)
            
            # Generate GenAI specific use cases
            genai_cases = self._generate_genai_use_cases(company_info)
            use_cases.extend(genai_cases)
            
            return use_cases
            
        except Exception as e:
            logger.error(f"❌ Use case generation failed: {str(e)}")
            return []
    
    def _generate_use_case_description(self, title: str, company_info: Dict) -> str:
        """Generate detailed description for a use case"""
        company_name = company_info.get('name', 'the company')
        industry = company_info.get('industry', 'their industry')
        
        descriptions = {
            'Automated Code Review and Quality Assurance': f"Implement AI-powered code review system for {company_name} to automatically detect bugs, security vulnerabilities, and code quality issues, reducing manual review time by 60%.",
            
            'Intelligent Customer Support Chatbots': f"Deploy advanced conversational AI to handle {company_name}'s customer inquiries, providing 24/7 support and reducing response time from hours to seconds.",
            
            'Predictive System Maintenance': f"Use machine learning to predict system failures and maintenance needs for {company_name}, reducing downtime and maintenance costs by up to 40%.",
            
            'Predictive Maintenance for Manufacturing Equipment': f"Implement IoT sensors and ML algorithms to predict equipment failures before they occur, helping {company_name} reduce unplanned downtime by 50%.",
            
            'Quality Control with Computer Vision': f"Deploy computer vision systems to automatically detect defects and quality issues in {company_name}'s production line, improving quality consistency.",
            
            'Medical Image Analysis and Diagnostics': f"Develop AI systems to assist {company_name} in analyzing medical images, improving diagnostic accuracy and reducing analysis time.",
            
            'Fraud Detection and Prevention': f"Implement real-time fraud detection systems using ML to protect {company_name} and its customers from financial fraud.",
            
            'Personalized Product Recommendations': f"Create AI-powered recommendation engine to provide personalized product suggestions for {company_name}'s customers, increasing sales conversion rates.",
            
            'Supply Chain Optimization': f"Use AI to optimize {company_name}'s supply chain operations, improving delivery times and reducing costs through better demand forecasting."
        }
        
        return descriptions.get(title, f"Implement {title.lower()} solution for {company_name} to improve operational efficiency and customer experience in the {industry} sector.")
    
    def _determine_category(self, title: str) -> str:
        """Determine the category of a use case"""
        categories = {
            'Operations': ['maintenance', 'optimization', 'planning', 'monitoring', 'quality control'],
            'Customer Experience': ['customer', 'support', 'chatbot', 'recommendation', 'personalization'],
            'Product Innovation': ['development', 'analysis', 'discovery', 'innovation', 'research'],
            'Risk Management': ['fraud', 'security', 'compliance', 'risk', 'safety'],
            'Analytics & Insights': ['analytics', 'prediction', 'forecasting', 'intelligence', 'insights']
        }
        
        title_lower = title.lower()
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'Operations'  # Default category
    
    def _determine_technology_stack(self, title: str) -> List[str]:
        """Determine technology stack for a use case"""
        tech_mapping = {
            'chatbot': ['Natural Language Processing', 'Conversational AI', 'Large Language Models'],
            'vision': ['Computer Vision', 'Deep Learning', 'Image Processing'],
            'predictive': ['Machine Learning', 'Time Series Analysis', 'Statistical Modeling'],
            'recommendation': ['Collaborative Filtering', 'Deep Learning', 'Recommendation Systems'],
            'fraud': ['Anomaly Detection', 'Machine Learning', 'Real-time Processing'],
            'maintenance': ['IoT Sensors', 'Predictive Analytics', 'Machine Learning'],
            'optimization': ['Operations Research', 'Machine Learning', 'Optimization Algorithms']
        }
        
        title_lower = title.lower()
        
        for keyword, technologies in tech_mapping.items():
            if keyword in title_lower:
                return technologies
        
        return ['Machine Learning', 'Data Analytics', 'Cloud Computing']  # Default stack
    
    def _assess_business_value(self, title: str, company_info: Dict) -> str:
        """Assess business value of a use case"""
        value_mapping = {
            'customer': 'High - Improves customer satisfaction and retention',
            'maintenance': 'High - Reduces operational costs and downtime',
            'fraud': 'Very High - Prevents financial losses',
            'optimization': 'Medium - Improves operational efficiency',
            'quality': 'High - Reduces defects and improves brand reputation',
            'recommendation': 'High - Increases sales and customer engagement',
            'analytics': 'Medium - Provides actionable business insights'
        }
        
        title_lower = title.lower()
        
        for keyword, value in value_mapping.items():
            if keyword in title_lower:
                return value
        
        return 'Medium - Provides operational improvements'
    
    def _assess_complexity(self, title: str) -> str:
        """Assess implementation complexity"""
        complexity_mapping = {
            'chatbot': 'Medium',
            'vision': 'High',
            'predictive': 'Medium',
            'recommendation': 'Medium',
            'fraud': 'High',
            'maintenance': 'High',
            'optimization': 'High',
            'analytics': 'Low'
        }
        
        title_lower = title.lower()
        
        for keyword, complexity in complexity_mapping.items():
            if keyword in title_lower:
                return complexity
        
        return 'Medium'
    
    def _estimate_timeline(self, title: str) -> str:
        """Estimate implementation timeline"""
        timeline_mapping = {
            'chatbot': '3-4 months',
            'vision': '6-8 months',
            'predictive': '4-6 months',
            'recommendation': '3-5 months',
            'fraud': '6-9 months',
            'maintenance': '6-12 months',
            'optimization': '8-12 months',
            'analytics': '2-3 months'
        }
        
        title_lower = title.lower()
        
        for keyword, timeline in timeline_mapping.items():
            if keyword in title_lower:
                return timeline
        
        return '4-6 months'
    
    def _generate_genai_use_cases(self, company_info: Dict) -> List[Dict]:
        """Generate specific GenAI use cases"""
        company_name = company_info.get('name', 'the company')
        
        genai_cases = [
            {
                'id': 'GenAI_01',
                'title': 'Intelligent Document Processing',
                'description': f"Implement GenAI solution for {company_name} to automatically extract, analyze, and summarize information from documents, contracts, and reports.",
                'category': 'Operations',
                'technology': ['Large Language Models', 'Document AI', 'Natural Language Processing'],
                'business_value': 'High - Reduces manual processing time by 70%',
                'implementation_complexity': 'Medium',
                'timeline': '3-4 months'
            },
            {
                'id': 'GenAI_02',
                'title': 'AI-Powered Content Generation',
                'description': f"Deploy generative AI to create marketing content, product descriptions, and communication materials for {company_name}.",
                'category': 'Customer Experience',
                'technology': ['Large Language Models', 'Content Generation', 'Creative AI'],
                'business_value': 'Medium - Accelerates content creation and improves consistency',
                'implementation_complexity': 'Low',
                'timeline': '2-3 months'
            },
            {
                'id': 'GenAI_03',
                'title': 'Automated Report Generation',
                'description': f"Use GenAI to automatically generate business reports, summaries, and insights from {company_name}'s data sources.",
                'category': 'Analytics & Insights',
                'technology': ['Large Language Models', 'Data Analytics', 'Report Automation'],
                'business_value': 'High - Saves 20+ hours per week on report creation',
                'implementation_complexity': 'Medium',
                'timeline': '3-5 months'
            }
        ]
        
        return genai_cases
    
    def _categorize_use_cases(self, use_cases: List[Dict]) -> List[Dict]:
        """Categorize use cases and add category-specific metadata"""
        for use_case in use_cases:
            category = use_case.get('category', 'Operations')
            
            # Add category-specific metadata
            if category == 'Operations':
                use_case['metrics'] = ['Cost Reduction', 'Efficiency Improvement', 'Process Automation']
            elif category == 'Customer Experience':
                use_case['metrics'] = ['Customer Satisfaction', 'Response Time', 'Engagement Rate']
            elif category == 'Product Innovation':
                use_case['metrics'] = ['Time to Market', 'Innovation Rate', 'Quality Improvement']
            else:
                use_case['metrics'] = ['ROI', 'Performance Improvement', 'Risk Reduction']
        
        return use_cases
    
    def _assess_use_cases(self, use_cases: List[Dict], company_info: Dict) -> List[Dict]:
        """Assess use cases for feasibility and impact"""
        for use_case in use_cases:
            # Add feasibility score (1-10)
            complexity = use_case.get('implementation_complexity', 'Medium')
            if complexity == 'Low':
                use_case['feasibility_score'] = 8
            elif complexity == 'Medium':
                use_case['feasibility_score'] = 6
            else:  # High
                use_case['feasibility_score'] = 4
            
            # Add impact score (1-10)
            business_value = use_case.get('business_value', '')
            if 'Very High' in business_value:
                use_case['impact_score'] = 9
            elif 'High' in business_value:
                use_case['impact_score'] = 7
            else:
                use_case['impact_score'] = 5
            
            # Calculate priority score
            use_case['priority_score'] = (use_case['feasibility_score'] + use_case['impact_score']) / 2
        
        return use_cases
    
    def _prioritize_use_cases(self, use_cases: List[Dict]) -> List[Dict]:
        """Prioritize use cases based on feasibility and impact"""
        # Sort by priority score (descending)
        prioritized = sorted(use_cases, key=lambda x: x.get('priority_score', 0), reverse=True)
        
        # Add priority ranking
        for i, use_case in enumerate(prioritized):
            use_case['priority_rank'] = i + 1
            
            if i < 3:
                use_case['priority_level'] = 'High Priority'
            elif i < 6:
                use_case['priority_level'] = 'Medium Priority'
            else:
                use_case['priority_level'] = 'Low Priority'
        
        return prioritized
    
    def _create_use_case_summary(self, use_cases: List[Dict]) -> str:
        """Create summary of generated use cases"""
        try:
            total_cases = len(use_cases)
            categories = {}
            
            for use_case in use_cases:
                category = use_case.get('category', 'Unknown')
                categories[category] = categories.get(category, 0) + 1
            
            high_priority = sum(1 for uc in use_cases if uc.get('priority_level') == 'High Priority')
            
            summary = f"""
Use Case Generation Summary:

Total Use Cases: {total_cases}
High Priority Cases: {high_priority}

Category Breakdown:
"""
            
            for category, count in categories.items():
                summary += f"- {category}: {count} use cases\n"
            
            summary += f"""
Top 3 Recommended Use Cases:
"""
            
            for i, use_case in enumerate(use_cases[:3]):
                summary += f"{i+1}. {use_case.get('title', 'Unknown')}\n"
            
            return summary.strip()
            
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    def _perform_search(self, query: str, max_results: int = 3) -> List[Dict]:
        """Perform search using Tavily API"""
        try:
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "basic",
                "include_images": False,
                "max_results": max_results
            }
            
            response = requests.post(self.base_url, json=payload, timeout=20)
            
            if response.status_code == 200:
                results = response.json()
                return results.get('results', [])
            else:
                return []
                
        except Exception as e:
            logger.warning(f"⚠️ Search failed: {str(e)}")
            return []
    
    def _create_fallback_use_cases(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback use cases when analysis fails"""
        company_info = research_data.get('company_info', {})
        company_name = company_info.get('name', 'Unknown Company')
        industry = company_info.get('industry', 'Technology').lower()
        
        # Use template use cases
        template_cases = self.use_case_templates.get(industry, self.use_case_templates['technology'])
        
        fallback_cases = []
        for i, title in enumerate(template_cases[:5]):  # Limit to 5 cases
            use_case = {
                'id': f"FB_{i+1:02d}",
                'title': title,
                'description': f"Implement {title.lower()} for {company_name}",
                'category': self._determine_category(title),
                'technology': ['Machine Learning', 'Data Analytics'],
                'business_value': 'Medium - Expected operational improvements',
                'implementation_complexity': 'Medium',
                'timeline': '4-6 months',
                'feasibility_score': 6,
                'impact_score': 6,
                'priority_score': 6,
                'priority_rank': i + 1,
                'priority_level': 'Medium Priority'
            }
            fallback_cases.append(use_case)
        
        return {
            'industry_standards': {
                'industry': industry,
                'ai_maturity': 'Medium',
                'common_applications': ['Machine Learning', 'Automation'],
                'technology_trends': ['Cloud Computing', 'Analytics']
            },
            'use_cases': fallback_cases,
            'use_case_summary': f"Generated {len(fallback_cases)} fallback use cases for {company_name}",
            'implementation_priorities': fallback_cases
        }