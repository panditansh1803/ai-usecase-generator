import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class WebSearchTool:
    def __init__(self):
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev/search"
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
    
    def search(self, query, num_results=5):
        """Search web and return results"""
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': num_results
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            if response.status_code == 200:
                results = response.json()
                return self._extract_results(results)
            return []
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def _extract_results(self, results):
        """Extract relevant information from search results"""
        extracted = []
        
        if 'organic' in results:
            for result in results['organic']:
                extracted.append({
                    'title': result.get('title', ''),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', '')
                })
        
        return extracted
    
    def analyze_with_gemini(self, text, prompt):
        """Use Gemini to analyze text"""
        try:
            full_prompt = f"{prompt}\n\nText to analyze: {text}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return "Analysis failed"
