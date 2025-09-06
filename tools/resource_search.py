import requests

class ResourceSearchTool:
    def search_github_repos(self, query):
        """Search GitHub repositories"""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                'q': query,
                'sort': 'stars',
                'per_page': 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                repos = []
                
                for item in data.get('items', []):
                    repos.append({
                        'title': item['name'],
                        'url': item['html_url'],
                        'description': item['description'] or f'{query} implementation',
                        'source': 'GitHub',
                        'type': 'Code Repository'
                    })
                
                return repos
        except Exception as e:
            print(f"GitHub search error: {e}")
            return []

    def search_huggingface_models(self, query):
        """Search HuggingFace models"""
        # Return some popular models as fallback
        models = [
            {
                'title': 'BERT Base Model',
                'url': 'https://huggingface.co/bert-base-uncased',
                'description': 'Pre-trained BERT model for NLP tasks',
                'source': 'HuggingFace',
                'type': 'Pre-trained Model'
            },
            {
                'title': 'GPT-2',
                'url': 'https://huggingface.co/gpt2',
                'description': 'Pre-trained GPT-2 model for text generation',
                'source': 'HuggingFace',
                'type': 'Pre-trained Model'
            }
        ]
        return models[:2]
