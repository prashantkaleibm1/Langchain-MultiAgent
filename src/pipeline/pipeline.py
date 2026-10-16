from src.agents.agents import build_search_agent ,build_reader_agent,writer_chain,critic_chain

def run_research_pipeline(topic:str) -> dict:
    state={}
    # search agent working
    ########################################
    print("\n"+ "= "*50)
    print("step 1 --- search agent working....."+topic)
    print("="*50)
    
    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages" : [("user",f"Find recent and reliable information about {topic}")]
    })
    state["search_results"]=search_result['messages'][-1].content
    print("\n search results",state['search_results'])
    
    # Reader agent working
    #########################################
    print("\n"+ "= "*50)
    print("step 1 --- Reader agent scraping.....")
    print("="*50)
        
    reader_agent=build_reader_agent()
    reader_result=reader_agent.invoke({
            "messages" : [("user",
                          f"Based on the following results about '{topic}',"
                          f"Pick the most relevent URL and scrap it for deeper content. \n\n"
                          f"Search Results : \n {state['search_results'][:800]}"
                          )]
        })
    
    state['scraped_content'] = reader_result['messages'][-1].content
    print("\n scraped Content \n",state['scraped_content'])
    
    
     # Writer agent working
     #########################################
    print("\n"+ "= "*50)
    print("step 1 --- Writer agent writing final report.....")
    
    research_combined= (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
        
    state['report'] = writer_chain.invoke({
            "topic" : topic,
            "research_gathered" : research_combined
        })
        
    print("\n Final Report \n",state['report'])
    
    return state
    
    