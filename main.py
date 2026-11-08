"""Data Sense: an AI career counsellor for aspiring data analysts.

Run with:  streamlit run main.py
Needs GROQ_API_KEY in .env (see .env.example).
"""
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
TOPICS = ["SQL", "Data Visualization", "Python", "Career Roadmap", "Resume Tips"]

PROMPT = PromptTemplate(
    template=(
        "You are a data analyst career counsellor. The learner is focusing on {topic}.\n"
        "Give practical, specific guidance in at most 80 words.\n"
        "Question: {query}"
    ),
    input_variables=["topic", "query"],
)


@st.cache_resource
def get_chain():
    llm = ChatGroq(model=MODEL, temperature=0.7, max_tokens=200)
    return PROMPT | llm


def main():
    st.set_page_config(page_title="Data Sense: Career Guidance", layout="centered")
    st.title("💡 Data Sense: Career Guidance")
    st.subheader("Your interactive data analyst career counsellor")

    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is not set. Copy .env.example to .env and add your key.")
        st.stop()

    topic = st.sidebar.selectbox("Area of interest", TOPICS)
    question = st.text_area("What do you want to know about becoming a data analyst?")

    if st.button("Get career advice"):
        if not question.strip():
            st.warning("Please enter your question above.")
            return
        with st.spinner("Thinking..."):
            try:
                response = get_chain().invoke({"topic": topic, "query": question.strip()})
            except Exception as exc:  # show API errors to the user
                st.error(f"Could not get advice: {exc}")
                return
        st.write("### 📋 Here's the advice")
        st.success(response.content)


if __name__ == "__main__":
    main()
