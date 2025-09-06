import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class UseCaseGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
    
    def generate_use_cases(self, company_data, industry_data):
        """Generate relevant use cases using Gemini AI"""
        print(f"💡 Generating use cases for {company_data['industry']}...")
        
        # Create comprehensive prompt for Gemini
        use_case_prompt = f"""
        Generate 5 specific AI/ML use cases for {company_data['company_name']} in the {company_data['industry']} industry.

        Company Information:
        - Name: {company_data['company_name']}
        - Industry: {company_data['industry']}
        - Overview: {company_data['company_info']['overview'][:300]}

        Industry Context:
        - AI Trends: {industry_data.get('ai_analysis', '')[:300]}

        For each use case, provide:
        1. Title (concise, specific to the company)
        2. Description (2-3 sentences explaining the solution)
        3. Category (e.g., Operations, Customer Experience, etc.)
        4. Technology (specific AI/ML technologies needed)
        5. Expected Impact (business benefits)
        6. Priority Score (1-5, where 5 is highest priority)

        Format as JSON array with these exact fields:
        [
            {{
                "title": "Use Case Title",
                "description": "Detailed description",
                "category": "Category Name",
                "technology": "AI/ML Technologies",
                "impact": "Expected business impact",
                "score": 4
            }}
        ]

        Focus on realistic, implementable solutions that address real business needs for {company_data['company_name']}.
        """
        
        try:
            response = self.model.generate_content(use_case_prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to parse JSON, if it fails, create structured use cases
            import json
            try:
                # Clean the response to extract JSON
                json_start = response_text.find('[')
                json_end = response_text.rfind(']') + 1
                
                if json_start != -1 and json_end != -1:
                    json_text = response_text[json_start:json_end]
                    use_cases = json.loads(json_text)
                else:
                    # Fallback: create use cases from text
                    use_cases = self._parse_text_to_use_cases(response_text)
                
            except json.JSONDecodeError:
                # Fallback: create structured use cases from text
                use_cases = self._parse_text_to_use_cases(response_text)
            
            # Ensure we have 5 use cases
            if len(use_cases) < 5:
                use_cases.extend(self._get_fallback_use_cases(company_data['industry']))
            
            return use_cases[:5]  # Return top 5
            
        except Exception as e:
            print(f"Error generating use cases with Gemini: {e}")
            # Return fallback use cases
            return self._get_fallback_use_cases(company_data['industry'])
    
    def _parse_text_to_use_cases(self, text):
        """Parse Gemini text response into structured use cases"""
        # This is a simple parser - you can make it more sophisticated
        use_cases = []
        
        # Split by numbered items and extract information
        lines = text.split('\n')
        current_use_case = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for numbered items or clear titles
            if any(char.isdigit() for char in line[:5]) or line.startswith('**'):
                if current_use_case:
                    use_cases.append(current_use_case)
                current_use_case = {
                    'title': line.replace('*', '').strip(),
                    'description': '',
                    'category': 'AI/ML Implementation',
                    'technology': 'Machine Learning',
                    'impact': 'Improved efficiency',
                    'score': 3
                }
            elif current_use_case and line:
                current_use_case['description'] += line + ' '
        
        if current_use_case:
            use_cases.append(current_use_case)
        
        return use_cases
    
    def _get_fallback_use_cases(self, industry):
        """Fallback use cases based on industry"""
        fallback_cases = {
            "Technology/Cloud Computing": [
                {
                    'title': 'AI-Powered Code Assistant',
                    'description': 'Intelligent code completion and debugging system using large language models',
                    'category': 'Developer Tools',
                    'technology': 'Large Language Models, Code Analysis',
                    'impact': 'Faster development, reduced bugs',
                    'score': 4
                },
                {
                    'title': 'Intelligent Cloud Resource Optimization',
                    'description': 'ML system for automatic cloud resource scaling and cost optimization',
                    'category': 'Cloud Operations',
                    'technology': 'ML, Predictive Analytics',
                    'impact': 'Reduced costs, improved performance',
                    'score': 4
                }
            ],
            # Add more industry-specific fallbacks...
        }
        
        return fallback_cases.get(industry, [
            {
                'title': 'Intelligent Customer Support Chatbot',
                'description': 'AI-powered chatbot for automated customer service',
                'category': 'Customer Experience',
                'technology': 'Large Language Models, NLP',
                'impact': '24/7 support, reduced costs',
                'score': 3
            }
        ])
