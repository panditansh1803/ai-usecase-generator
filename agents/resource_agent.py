import requests
import json
import logging
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class ResourceAgent:
    """Agent responsible for collecting datasets, models, and implementation resources"""
    
    def __init__(self):
        self.kaggle_base_url = "https://www.kaggle.com/api/v1"
        self.github_search_url = "https://api.github.com/search/repositories"
        self.huggingface_base_url = "https://huggingface.co/api"
        
        # Predefined resource mappings for different use case types
        self.resource_mappings = {
            'chatbot': {
                'datasets': ['conversational-ai-datasets', 'customer-support-data', 'dialog-datasets'],
                'models': ['microsoft/DialoGPT', 'facebook/blenderbot', 'google/flan-t5'],
                'keywords': ['chatbot', 'conversational AI', 'dialog system']
            },
            'computer vision': {
                'datasets': ['image-classification', 'object-detection', 'industrial-defects'],
                'models': ['yolov5', 'resnet', 'efficientnet'],
                'keywords': ['computer vision', 'image classification', 'object detection']
            },
            'predictive analytics': {
                'datasets': ['time-series-forecasting', 'predictive-maintenance', 'sensor-data'],
                'models': ['prophet', 'lstm', 'xgboost'],
                'keywords': ['time series', 'forecasting', 'predictive maintenance']
            },
            'recommendation': {
                'datasets': ['recommendation-systems', 'collaborative-filtering', 'user-item-interactions'],
                'models': ['matrix-factorization', 'neural-collaborative-filtering'],
                'keywords': ['recommendation system', 'collaborative filtering', 'personalization']
            },
            'fraud detection': {
                'datasets': ['fraud-detection', 'credit-card-fraud', 'anomaly-detection'],
                'models': ['isolation-forest', 'autoencoder', 'xgboost'],
                'keywords': ['fraud detection', 'anomaly detection', 'financial fraud']
            }
        }
    
    def execute(self, combined_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute resource collection tasks"""
        try:
            use_cases = combined_data.get('use_cases', [])
            company_info = combined_data.get('company_info', {})
            
            logger.info(f"📚 Collecting resources for {len(use_cases)} use cases")
            
            # Collect resources for each use case
            all_resources = []
            kaggle_datasets = []
            huggingface_resources = []
            github_repos = []
            
            for use_case in use_cases:
                use_case_resources = self._collect_use_case_resources(use_case, company_info)
                all_resources.extend(use_case_resources['resources'])
                kaggle_datasets.extend(use_case_resources['kaggle_datasets'])
                huggingface_resources.extend(use_case_resources['huggingface_resources'])
                github_repos.extend(use_case_resources['github_repos'])
            
            # Remove duplicates and validate links
            unique_resources = self._deduplicate_resources(all_resources)
            validated_resources = self._validate_resource_links(unique_resources)
            
            # Create resource summary
            resource_summary = self._create_resource_summary(validated_resources)
            
            # Generate implementation guides
            implementation_guides = self._generate_implementation_guides(use_cases, validated_resources)
            
            results = {
                'resources': validated_resources,
                'kaggle_datasets': self._deduplicate_datasets(kaggle_datasets),
                'huggingface_resources': self._deduplicate_datasets(huggingface_resources),
                'github_repos': self._deduplicate_datasets(github_repos),
                'resource_summary': resource_summary,
                'implementation_guides': implementation_guides,
                'resource_categories': self._categorize_resources(validated_resources)
            }
            
            logger.info(f"✅ Collected {len(validated_resources)} resources")
            return results
            
        except Exception as e:
            logger.error(f"❌ Resource collection failed: {str(e)}")
            return self._create_fallback_resources(combined_data)
    
    def _collect_use_case_resources(self, use_case: Dict, company_info: Dict) -> Dict[str, List]:
        """Collect resources for a specific use case"""
        try:
            title = use_case.get('title', '').lower()
            category = use_case.get('category', '').lower()
            technologies = use_case.get('technology', [])
            
            resources = {
                'resources': [],
                'kaggle_datasets': [],
                'huggingface_resources': [],
                'github_repos': []
            }
            
            # Determine resource type based on use case
            resource_type = self._determine_resource_type(title, technologies)
            
            # Collect Kaggle datasets
            kaggle_datasets = self._search_kaggle_datasets(resource_type, title)
            resources['kaggle_datasets'].extend(kaggle_datasets)
            
            # Collect HuggingFace resources
            hf_resources = self._search_huggingface_resources(resource_type, technologies)
            resources['huggingface_resources'].extend(hf_resources)
            
            # Collect GitHub repositories
            github_repos = self._search_github_repos(resource_type, title)
            resources['github_repos'].extend(github_repos)
            
            # Combine all resources
            all_resources = []
            all_resources.extend([{**ds, 'source': 'Kaggle'} for ds in kaggle_datasets])
            all_resources.extend([{**ds, 'source': 'HuggingFace'} for ds in hf_resources])
            all_resources.extend([{**ds, 'source': 'GitHub'} for ds in github_repos])
            
            resources['resources'] = all_resources
            
            return resources
            
        except Exception as e:
            logger.warning(f"⚠️ Resource collection failed for use case: {str(e)}")
            return {'resources': [], 'kaggle_datasets': [], 'huggingface_resources': [], 'github_repos': []}
    
    def _determine_resource_type(self, title: str, technologies: List[str]) -> str:
        """Determine the type of resources needed based on use case"""
        title_lower = title.lower()
        tech_lower = ' '.join(technologies).lower()
        
        if any(keyword in title_lower for keyword in ['chatbot', 'conversational', 'customer support']):
            return 'chatbot'
        elif any(keyword in title_lower for keyword in ['vision', 'image', 'quality control']):
            return 'computer vision'
        elif any(keyword in title_lower for keyword in ['predictive', 'maintenance', 'forecasting']):
            return 'predictive analytics'
        elif any(keyword in title_lower for keyword in ['recommendation', 'personalization']):
         return "Recommendation Systems"  # Must be indented with 4 spaces or 1 tab
