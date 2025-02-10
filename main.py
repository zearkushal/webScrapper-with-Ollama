import streamlit as st
from scrape import scrap_website, split_dom_content, clean_body_content
from parse import parse_with_ollama

st.title("🌐 AI Web Scraper with Ollama")
URL = st.text_input("🔗 Enter the Website URL")

if st.button("📂 Scrap Site"):
    st.write("⏳ Scraping the website...")
    raw_body = scrap_website(URL)

    if raw_body:
        cleaned_content = clean_body_content(raw_body)
        st.session_state.dom_content = cleaned_content

        st.write("✅ Scraping complete!")
        with st.expander("📄 View Cleaned DOM Content:"):
            st.text_area("DOM Content", cleaned_content, height=300)
    else:
        st.error("❌ Failed to retrieve website content.")

if "dom_content" in st.session_state:
    parse_description = st.text_area("🔍 Describe what you want to extract")

    if st.button("📊 Parse Content"):
        if parse_description:
            st.write("⏳ Parsing the content...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)

            print(f"🟢 Final Parsed Result: {result}")

            st.session_state['parsed_output'] = result
            st.rerun()


if 'parsed_output' in st.session_state:
    st.subheader("📌 Extracted Information:")
    st.write(st.session_state['parsed_output'])
