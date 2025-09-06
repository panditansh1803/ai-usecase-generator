from tools.resource_search import ResourceSearchTool

class ResourceCollector:
    def __init__(self):
        self.search_tool = ResourceSearchTool()
    
    def collect_resources(self, use_cases):
        """Collect relevant datasets and resources for use cases"""
        print("📦 Collecting resources...")
        
        all_resources = []
        
        for use_case in use_cases:
            technology = use_case.get('technology', '').lower()
            
            # Search for GitHub repositories
            github_query = f"{technology} implementation"
            github_repos = self.search_tool.search_github_repos(github_query)
            all_resources.extend(github_repos)
            
            # Search for HuggingFace models
            if any(term in technology for term in ['llm', 'language model', 'nlp', 'bert']):
                hf_models = self.search_tool.search_huggingface_models('bert transformer')
                all_resources.extend(hf_models)
            
            if 'computer vision' in technology:
                hf_models = self.search_tool.search_huggingface_models('resnet vision')
                all_resources.extend(hf_models)
        
        # Remove duplicates
        unique_resources = []
        seen_urls = set()
        
        for resource in all_resources:
            if resource.get('url') and resource['url'] not in seen_urls:
                unique_resources.append(resource)
                seen_urls.add(resource['url'])
        
        return unique_resources[:8]
