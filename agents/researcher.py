import os
import google.generativeai as genai
from tools.web_search import WebSearchTool
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDmYw1Aj_1HnPKupL7dSV1fB9FDi6B-eDg"))

class ResearchAgent:
    def __init__(self):
        self.search_tool = WebSearchTool()
        self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
    
    def research_company(self, company_name):
        """Research company information"""
        print(f"🔍 Researching {company_name}...")
        
        # Multiple search queries for comprehensive research
        queries = [
            f"{company_name} business model revenue 2024",
            f"{company_name} main products services",
            f"{company_name} industry sector",
            f"what does {company_name} company do"
        ]
        
        all_results = []
        for query in queries:
            results = self.search_tool.search(query, 3)
            all_results.extend(results)
        
        # Use Gemini to analyze company information
        search_text = " ".join([f"{r['title']} {r['snippet']}" for r in all_results[:10]])
        
        company_analysis_prompt = f"""
        Analyze the following information about {company_name} and provide:
        1. Company overview (2-3 sentences)
        2. Industry classification
        3. Main products/services (list 3-5)
        4. Business model type
        
        Keep it concise and factual.
        """
        
        analysis = self.search_tool.analyze_with_gemini(search_text, company_analysis_prompt)
        
        # Extract industry from analysis
        industry = self._extract_industry_from_analysis(analysis, company_name)
        
        return {
            'company_name': company_name,
            'industry': industry,
            'company_info': {
                'overview': analysis[:500] + '...',
                'products': [r['title'] for r in all_results[:5]],
                'analysis': analysis
            },
            'sources': [r['link'] for r in all_results[:5]]
        }
    
    def research_industry_trends(self, industry):
        """Research industry trends and AI adoption"""
        print(f"📊 Researching {industry} industry trends...")
        
        queries = [
            f"{industry} AI adoption trends 2024",
            f"{industry} digital transformation challenges",
            f"AI use cases {industry} industry",
            f"{industry} technology opportunities 2025"
        ]
        
        all_results = []
        for query in queries:
            results = self.search_tool.search(query, 3)
            all_results.extend(results)
        
        # Use Gemini to analyze industry trends
        search_text = " ".join([f"{r['title']} {r['snippet']}" for r in all_results[:10]])
        
        trend_analysis_prompt = f"""
        Based on the search results about {industry}, provide:
        1. Top 5 industry trends for 2024-2025
        2. Main challenges facing the industry
        3. AI adoption patterns
        4. Digital transformation opportunities
        
        Format as clear bullet points.
        """
        
        trend_analysis = self.search_tool.analyze_with_gemini(search_text, trend_analysis_prompt)
        
        return {
            'industry': industry,
            'trends': [r['title'] for r in all_results[:5]],
            'challenges': [r['snippet'][:100] + '...' for r in all_results[:3]],
            'ai_analysis': trend_analysis,
            'sources': [r['link'] for r in all_results[:5]]
        }
    
    def _extract_industry_from_analysis(self, analysis, company_name):
        """Extract industry from Gemini analysis"""
        analysis_lower = analysis.lower()
        
        # Industry classification based on keywords in analysis
        if any(word in analysis_lower for word in ['cloud', 'software', 'technology', 'saas', 'platform']):
            return "Technology/Cloud Computing"
        elif any(word in analysis_lower for word in ['search', 'advertising', 'social media', 'internet']):
            return "Technology/Internet Services"
        elif any(word in analysis_lower for word in ['manufacturing', 'factory', 'production', 'automotive']):
            return "Manufacturing"
        elif any(word in analysis_lower for word in ['finance', 'bank', 'financial', 'payment']):
            return "Financial Services"
        elif any(word in analysis_lower for word in ['healthcare', 'medical', 'pharmaceutical', 'hospital']):
            return "Healthcare"
        elif any(word in analysis_lower for word in ['retail', 'e-commerce', 'shopping', 'consumer']):
            return "Retail/E-commerce"
        else:
            return "Technology"  # Default fallback
