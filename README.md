# Data Sense: Career Guidance

**An AI career counsellor for aspiring data analysts.** Pick an area (SQL, data visualization, Python, career roadmap or résumé tips), ask a question, and get short, practical advice from a Llama 3.3 model on Groq.

## How it works

The Streamlit app sends your question and chosen topic to a LangChain prompt, which calls the Groq API and shows the answer.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # add your Groq API key
streamlit run main.py
```

## License

MIT, see [LICENSE](LICENSE). Built by [Lavanya Srivastava](https://github.com/lavanya1402), Lavanya AI Consultancy.
