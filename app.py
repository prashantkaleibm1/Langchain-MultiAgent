import streamlit as st
from src.pipeline.pipeline import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Multi-Agent Research Assistant")
st.caption("Developed by Prashant Kale")
st.caption("Search → Reader → Writer")

st.markdown(
    "Enter a research topic. The pipeline searches for sources, scrapes relevant content, "
    "and drafts a report based on the gathered research."
)

with st.form("research_form"):
    topic = st.text_area(
        "Research topic",
        placeholder="e.g. Recent applications of Generative AI in software development",
        height=100,
    )
    submitted = st.form_submit_button(
        "Run Research Pipeline",
        type="primary",
        use_container_width=True,
    )

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        try:
            with st.spinner("Running Search, Reader, and Writer agents. This may take a while..."):
                result = run_research_pipeline(topic.strip())

            if not isinstance(result, dict):
                st.error("The pipeline did not return a dictionary.")
            else:
                st.success("Research pipeline completed.")

                search_results = result.get("search_results", "No search results returned.")
                scraped_content = result.get("scraped_content", "No scraped content returned.")
                report = result.get("report", "No report returned.")

                tab_search, tab_reader, tab_report, tab_raw = st.tabs(
                    ["🔍 Search Results", "📄 Scraped Content", "📝 Final Report", "🧾 Full Result"]
                )

                with tab_search:
                    st.subheader("Search Agent Results")
                    st.text_area(
                        "Search results",
                        value=str(search_results),
                        height=420,
                        disabled=True,
                        label_visibility="collapsed",
                    )

                with tab_reader:
                    st.subheader("Reader Agent Output")
                    st.text_area(
                        "Scraped content",
                        value=str(scraped_content),
                        height=420,
                        disabled=True,
                        label_visibility="collapsed",
                    )

                with tab_report:
                    st.subheader("Writer Agent Report")
                    st.markdown(str(report))
                    st.download_button(
                        "Download report (.md)",
                        data=str(report),
                        file_name="research_report.md",
                        mime="text/markdown",
                        use_container_width=False,
                    )

                with tab_raw:
                    st.json(result)

        except Exception as exc:
            st.error("The research pipeline failed.")
            st.exception(exc)

st.divider()
st.caption(
    "Note: this interface runs the current pipeline as written. "
    "The Critic Chain is imported in pipeline.py but is not currently invoked."
)
