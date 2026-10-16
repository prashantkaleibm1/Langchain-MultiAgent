from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # STEP 1: SEARCH AGENT
    print("\n" + "= " * 50)
    print(f"Step 1 --- Search agent working: {topic}")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [
            ("user", f"Find recent and reliable information about {topic}")
        ]
    })

    state["search_results"] = search_result["messages"][-1].content
    print("\nSearch results:\n", state["search_results"])

    # STEP 2: READER AGENT
    print("\n" + "= " * 50)
    print("Step 2 --- Reader agent scraping...")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following results about '{topic}', "
                "pick relevant URLs and scrape them for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content
    print("\nScraped content:\n", state["scraped_content"])

    # Combine the evidence for the Writer and Critic chains.
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["research"] = research_combined

    # STEP 3: WRITER CHAIN
    print("\n" + "= " * 50)
    print("Step 3 --- Writer agent writing final report...")
    print("=" * 50)

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research_gathered": research_combined,
    })
    print("\nFinal report:\n", state["report"])

    # STEP 4: CRITIC / REVIEWER CHAIN
    print("\n" + "= " * 50)
    print("Step 4 --- Critic agent reviewing the report...")
    print("=" * 50)

    state["critic_review"] = critic_chain.invoke({
        "topic": topic,
        "research_gathered": research_combined,
        "report": state["report"],
    })
    print("\nCritic review:\n", state["critic_review"])

    return {
        "topic": topic,
        "search_results": state["search_results"],
        "scraped_content": state["scraped_content"],
        "research": state["research"],
        "report": state["report"],
        "critic_review": state["critic_review"],
    }
