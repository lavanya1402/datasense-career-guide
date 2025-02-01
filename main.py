import os
import subprocess
import threading
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
load_dotenv()

# Streamlit app content
streamlit_code = """
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Prompt template for career guidance
prompt = '''You are a data analyst career counselor. Provide concise guidance in 50 words maximum.
The user query is: {query}'''

prompt_template = PromptTemplate(
    template=prompt,
    input_variables=["query"]
)

# Initialize ChatGroq
llm = ChatGroq(temperature=0.7, model="llama3-70b-8192", max_tokens=50)

chain = prompt_template | llm

# Streamlit UI
def main():
    st.set_page_config(page_title="Data Sense: Career Guidance", layout="centered")
    st.title("💡 Data Sense: Career Guidance")
    st.subheader("Your Interactive Data Analyst Career Counselor")
    st.markdown("Ask your career-related questions and get expert AI advice tailored for aspiring data analysts!")

    # Input form
    st.sidebar.header("👩‍💻 User Options")
    st.sidebar.write("Choose your area of interest:")
    interests = st.sidebar.selectbox("Select an area:", 
                                      ["SQL", "Data Visualization", "Python", "Career Roadmap", "Resume Tips"])

    st.sidebar.write("Need additional help?")
    st.sidebar.checkbox("Schedule a 1:1 session")

    st.write("### 🤔 Ask a Career Question")
    question = st.text_area("What do you want to know about becoming a data analyst?", "")
    
    if st.button("Get Career Advice"):
        if question.strip():
            try:
                response = chain.invoke({"query": question})
                st.write("### 📋 Here's the advice:")
                st.success(response.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter your question above.")

    st.write("### 📝 Provide Feedback")
    feedback = st.text_input("How helpful was the advice?")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
"""

# Function to run Streamlit app in a separate thread
def run_streamlit():
    with NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(streamlit_code.encode())
        temp_file.flush()
        try:
            subprocess.run(["streamlit", "run", temp_file.name])
        finally:
            os.unlink(temp_file.name)

if __name__ == "__main__":
    thread = threading.Thread(target=run_streamlit)
    thread.start()
    thread.join()