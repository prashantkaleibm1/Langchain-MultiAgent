from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search,scrape_url
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()

# Model Initialize     #######

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0)

# First Agent is Search Agent #######

def build_search_agent():
    # prompt template
    return create_agent(
        model=llm,
        tools=[web_search]
    )

# Second Agent is Scrape(Reader) Agent #######

def build_reader_agent():
    # prompt template
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


#  Writer Chain ####################
parser = StrOutputParser()
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a professional research report writer.

        Prepare a factual, well-organized report using only
        the supplied research and its source details.

        Use exactly these sections:

        # Introduction
        Introduce the topic and explain its context and purpose.

        # Key Findings
        Present the most important findings as numbered points.
        Explain each finding clearly.
        Cite the relevant source inline using [1], [2], etc.

        # Sources
        List the sources and URLs actually provided in the research.
        Include their titles, URLs, and publication details
        when available. Number them to match inline citations.

        Important rules:
        - Never invent facts, URLs, citations, or publication dates.
        - If source details are missing, say "Source details not provided".
        - Clearly distinguish evidence from assumptions.
        - If the research is insufficient, state the limitation.
        """
    ),
    (
        "human",
        """
        Topic:
        {topic}

        Research Gathered:
        {research_gathered}

        Write the report using the required structure.
        """
    )
])

writer_chain = writer_prompt | llm | parser


#  Critic(Reviewer) Chain ####################

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a professional research report reviewer.

        Evaluate the report against the provided topic and research.

        Return exactly these four sections:

        # Report
        Provide the complete revised report with:
        1. Introduction
        2. Key Findings
        3. Sources

        # Score
        Give an overall score out of 10.
        Evaluate:
        - Factual accuracy and research support: 0-3
        - Completeness of findings: 0-2
        - Structure and organization: 0-2
        - Clarity and grammar: 0-1
        - Source quality and citation consistency: 0-2

        Explain the score briefly.

        # Strengths
        List specific strengths of the report.

        # Areas to Improve
        List weaknesses and actionable improvements.

        Rules:
        - Check whether the report answers the given topic.
        - Compare claims against the supplied research.
        - Do not invent facts, citations, or URLs.
        - Preserve valid findings and improve unclear content.
        - Identify missing evidence rather than guessing.
        - Return all four sections, even if some feedback is limited.
        """
    ),
    (
        "human",
        """
        TOPIC:
        {topic}

        RESEARCH GATHERED:
        {research_gathered}

        WRITER'S DRAFT:
        {report}

        Review the draft in the context of the topic and research.
        Return the complete revised report, score, strengths,
        and areas to improve.
        """
    )
])

critic_chain = critic_prompt | llm | parser

