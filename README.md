# LangChain Multi-Agent Research Assistant

A research assistant that searches the web, reads relevant pages, and writes a sourced report. A second GUI mode also reviews the report and provides a score and improvement suggestions.

## Requirements

- Python 3.11
- Conda (recommended) or another Python environment manager
- An OpenAI API key
- A Tavily API key

## Create the environment

From the project root, run these commands in Anaconda Prompt or PowerShell with Conda available:

```powershell
conda create -n langagent python=3.11 -y
conda activate langagent
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your API keys:

```dotenv
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keep `.env` private and do not commit API keys. `OPENAI_API_KEY` is read by LangChain's OpenAI integration; `TAVILY_API_KEY` is used by the web-search tool.

## Models and technologies

- **Model:** OpenAI `gpt-4o-mini`, configured with temperature `0` for the agents and report chains.
- **Agent and LLM framework:** LangChain, `langchain-core`, `langchain-community`, and `langchain-openai`.
- **Local GUI:** Streamlit.
- **Web search:** Tavily Search API via `tavily-python`.
- **Page retrieval and extraction:** Requests fetches web pages; Beautiful Soup extracts page content. `readability-lxml` and `trafilatura` are included as scraping-related dependencies, though the current scraper uses Requests and Beautiful Soup.
- **Configuration and diagnostics:** `python-dotenv` loads the `.env` file; Rich formats console output.

## Tools and pipeline

The LangChain search agent can call:

- **`web_search(query)`** uses Tavily to find up to five results and returns each result's title, URL, and snippet.
- **`scrape_url(url)`** retrieves a page with Requests and tries to extract its main content, article text, headings, and paragraphs with Beautiful Soup. It returns a readable error message for common request failures.

The standard pipeline in `src/pipeline/pipeline.py` runs three stages:

1. **Search:** the search agent finds recent, relevant sources.
2. **Reader:** the reader agent selects relevant result URLs and scrapes page content.
3. **Writer:** a prompt chain turns the search results and scraped content into a report with an introduction, numbered key findings, and cited sources.

The optional pipeline in `src/pipeline/pipeline_critic.py` runs those same stages, then adds a **Critic** review. The critic returns a revised report, an overall score out of 10, strengths, and actionable areas to improve. It is available through `app_critic.py`.

## Run the local GUI

Activate the environment, then from the project root run:

```powershell
conda activate langagent
streamlit run app.py
```

Streamlit opens the standard Search → Reader → Writer GUI in your browser. To use the version with the Critic review tab instead, run:

```powershell
streamlit run app_critic.py
```

## Run from the command line

The included `main.py` runs the standard pipeline for the sample topic defined in that file and prints progress and results in the terminal:

```powershell
conda activate langagent
python main.py
```

To research a different topic from Python, call `run_research_pipeline("your topic")` from `src.pipeline.pipeline`. For the version that includes review, import it from `src.pipeline.pipeline_critic`.
