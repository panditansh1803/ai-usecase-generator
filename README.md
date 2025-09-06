# Multi-Agent AI Use Case Generator

A multi-agent system that conducts market research and generates AI & Generative AI use cases for companies or industries. It automates research, use case creation, resource collection, and proposal writing using AI models like Google Gemini.

---

## Motivation

This project aims to streamline the identification of relevant AI/ML use cases for organizations by leveraging a modular multi-agent architecture that performs:

- Company and industry research
- AI use case generation with GenAI solutions
- Collection of relevant resources (datasets, models, code)
- Automated proposal generation with references and feasibility analysis

---

## Project Architecture

The system consists of four specialized agents:

1. **Research Agent**: Performs web and AI-powered research on companies and sectors.
2. **Use Case Generator**: Produces AI/ML use cases tailored to the business and industry.
3. **Resource Collector**: Gathers datasets and code repositories from Kaggle, HuggingFace, and GitHub.
4. **Proposal Writer**: Creates comprehensive, reference-backed reports and outputs.

Data flows sequentially through these agents to produce actionable AI proposals.

![Architecture Diagram](https://drive.google.com/file/d/1IIG_uzKc_knOQAUv-OuiBazEgzI99mne/view?usp=drive_link) 

---

## Usage Instructions

### Setup

1. Clone this repository.
2. Create a `.env` file in the root directory with the following keys:
GOOGLE_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key

text
3. Install Python dependencies:
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

text

### Running the Program

- **Interactive Mode:**  
Run `python main.py` and follow CLI prompts.

- **Command Line Mode:**  
Run `python main.py <company_name> [industry]`  
Example:  
python main.py Microsoft Technology

text

---

## Project Structure

ai-usecase-generator/
├── agents/
│ ├── researcher.py
│ ├── use_case_generator.py
│ ├── resource_collector.py
│ └── proposal_writer.py
├── tools/
│ ├── web_search.py
│ └── resource_search.py
├── outputs/ # Generated proposals and resource files saved here
├── main.py
├── requirements.txt
└── .env # Stores API keys (not in version control)

text

---

## Dependencies

- Python 3.10+
- google-generativeai
- requests
- python-dotenv

*(See `requirements.txt` for full list)*

---

## Challenges and Future Work

- Enhancing coverage of diverse industries
- Adding advanced memory and personalization capabilities
- Deploying on Streamlit or Gradio for web-based interaction
- Improving fallback handling and robustness under API limitations

---

## Credits

Built based on deep learning and multi-agent frameworks including:
- Google Gemini AI
- CrewAI & LangChain libraries
- OpenAI community insights

---

## License

Specify your license here (e.g., MIT License). See https://choosealicense.com/ for help.

---

## Contact

Ansh Vashistha – vashisthaansh1803@gmail.com  
